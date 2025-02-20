# Copyright (c) 2024-2025 Cary Miller
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
# THIS SOFTWARE.

import json
import jsonref
from jsonschema import FormatChecker
import httpx
from . tools import (dvalidator, parsed_file_or_url, identity_func,
                   extract_from_dict_list,
                   retry_call,
                   LocalValidationError,
                   raw_file_or_url,
                   )

class ValidDataBadResponse(LocalValidationError): pass

class SurpriseArgs(Exception): pass
class NonDictArgs(SurpriseArgs): pass
class ListArgs(SurpriseArgs): pass

class BadEndpointOrVerb(Exception): pass


def parameters_to_schema(ev_info):
    if 'parameters' in ev_info:
        parameters = ev_info['parameters']
    pr = extract_from_dict_list(parameters or {}, 'required')
    return {
        'required': [key for key in pr if pr[key]],
        'properties': extract_from_dict_list(parameters or {}, 'schema'), 
        'additionalProperties': False, 
        'type': 'object',
    }


def dynamic_validator(config):
    local_validate = config.validate
    jdoc = jsonref.loads(json.dumps(parsed_file_or_url(config.swagger_path)))
    paths = config.alt_swagger(jdoc)['paths']

    def validator(endpoint, verb='get'):
        """Return a validator for `(endpoint, verb)`.
        """
        try:
            schema = parameters_to_schema(paths[endpoint][verb])
        except KeyError as exc:
            raise BadEndpointOrVerb(exc.args[0])
        return dvalidator(local_validate)(schema, format_checker=FormatChecker())
    return validator


def dynamic_call(config):
    prepped = prep_func(config)

    @retry_call()
    def call(endpoint, verb, params):
        """Call (endpoint, verb) with params. """
        (url, verb, request_params) = prepped(endpoint, verb, params)
        request = httpx.Request(verb, url, **request_params)
        with httpx.Client() as client:
            return client.send(request)  
    return call


def prep_func(config):
    jdoc = jsonref.loads(json.dumps(parsed_file_or_url(config.swagger_path)))
    paths = config.alt_swagger(jdoc)['paths']
    head_func = config.head_func

    def prepped(endpoint, verb, args):
      try:
        """Prepare args for endpoint, verb.
        """
        if not args:
            return (config.api_base + endpoint, verb, {})
        if type(args) is not dict:
            raise NonDictArgs(f'{endpoint} {verb} {args}')

        ev_params = paths[endpoint][verb]['parameters'] or {}
        location = extract_from_dict_list(ev_params, 'in')
        request_params = {}
        query = {}
        form_data = {}
        files = {}
        data = {}
        headers = {}

        assert type(args) is dict
        for arg in args:
            plocation = location[arg]
            if '{'+str(arg)+'}' in endpoint:
                plocation = 'path'

            if plocation == 'path':
                endpoint = endpoint.replace('{'+arg+'}', str(args[arg]))
            elif plocation == 'query':
                query[arg] = args[arg]
            elif plocation == 'header':
                headers[arg] = args[arg]
            elif plocation == 'formData':
                form_data[arg] = args[arg]
            elif plocation == 'files':
                files[arg] = args[arg]
            elif plocation == 'data':
                data[arg] = args[arg]

        if query:
            request_params['params'] = query
        if verb in 'post put' and 'params' in request_params:
            request_params = {'json': request_params['params']}
        if headers:
            request_params['headers'] = headers
        if data:
            request_params['data'] = data
        if files:
            request_params['files'] = files

        heads = head_func(endpoint, verb) if head_func else {}
        if heads:
            if not 'headers' in request_params:
                request_params['headers'] = {}
            request_params['headers'].update(heads)

        return (config.api_base + endpoint, verb, request_params)
      finally:
        pass
    return prepped

