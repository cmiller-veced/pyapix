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

from datetime import datetime

from . import api_tools
from .api_tools import (dynamic_validator, dynamic_call, SurpriseArgs)
from .api_tools import *
from .tools import (LocalValidationError, ValidDataBadResponse, )
from .info import local

class Foo(LocalValidationError): pass


def local_validate(params):
    """Catch data problems missed by the schema.
    # eg start_date > end_date
    params = {
        'start': '2024-09-17T18:39:00+00:00', 
        'end':   '2024-09-18T18:39:00+00:00',
    }
    """
    fmt = '%Y-%m-%dT%H:%M:%S+00:00'


def param_func(pdict):
  try:
    """
    Extract info for inserting into schema.
    """
    d = {}
#    for key in ['required', 'name', 'schema', 'type']:
    for key in ['required', 'name', 'schema']:
        if key in pdict:
            d[key] = pdict[key]
    if 'schema' not in d:
        d['schema'] = {}
        for key in ['format', 'enum', 'type', 'items', 'default']:
            if key in pdict:
                d['schema'][key] = pdict[key]

        # below is required because otherwise we get a jsonschema error...
        # jsonschema.exceptions.UnknownType: Unknown type 'file'
        if d['schema']['type'] == 'file': 
            d['schema']['type'] = 'string'

    return d
  finally:
    pass


def altered_raw_swagger(jdoc):
  try:
    """Alter raw data to conform with local code assumptions.
    This function takes a swagger doc as a json and returns json.
    """
    for endpoint in jdoc['paths']:
        epdoc = jdoc['paths'][endpoint]
        for verb in epdoc:
            vdoc = epdoc[verb]
            parameters = vdoc['parameters']
            jdoc['paths'][endpoint][verb]['parameters'] = [param_func(d) for d in parameters]
            if (endpoint, verb) == ('/pet/findByStatus', 'get'):
                foop = parameters
    return jdoc
  finally:
    pass



def prep_func(config):
    jdoc = jsonref.loads(json.dumps(parsed_file_or_url(config.swagger_path)))
    paths = config.alt_swagger(jdoc)['paths']
    head_func = config.head_func

    def prepped(endpoint, verb, args):
      try:
        """
        """
        if not args:
            return (config.api_base + endpoint, verb, {})
        if type(args) not in (dict, list, str):
            raise Exception(f'{endpoint} {verb} {args}')
        if type(args) is not dict:
            raise NonDictArgs(f'{endpoint} {verb} {args}')

        ev_params = paths[endpoint][verb]['parameters'] or {}
        location = extract_from_dict_list(ev_params, 'in')
        print('prepped')
        print(endpoint, verb, list(ev_params))
        print('location', location)
        print('......')
        request_params = {}
        query = {}
        form_data = {}
        files = {}
        data = {}
        headers = {}

        assert type(args) is dict
        print()
        print(f'xx ep: {endpoint}  verb: {verb}')
        for arg in args:

            # TODO: 'query' is not a good default.
            # TODO: 'query' is not a good default.
            plocation = location[arg] if arg in location else 'query'
            # TODO: 'query' is not a good default.
            # TODO: 'query' is not a good default.
            # TODO: change altered_raw_swagger to always have location.
            # because there should not be a default anyway.
            if '{'+str(arg)+'}' in endpoint:
                plocation = 'path'

            # TMP    #  petstore-specific    #  petstore-specific
            if arg == 'file':                  #  petstore-specific
                plocation = 'files'         #  petstore-specific
            if arg == 'additionalMetadata':    #  petstore-specific
                plocation = 'data'             #  petstore-specific
                # TODO: find another API that does file uploads.
            # TMP    #  petstore-specific    #  petstore-specific

            #  petstore-specific
            if endpoint.startswith('/pet') and verb == 'post': 
                sp = endpoint.split('/')
                if len(sp) == 3:
                    try:
                        int(sp[-1])
                        print('yoohoo')
                        plocation = 'data'             #  petstore-specific
                    except ValueError:
                        pass
                print(endpoint, sp, arg)
                
            print(f'xx arg: {arg}  plocation: {plocation}')

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

        print()
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


def parameters_to_schema(ev_info):
  try:
    if 'parameters' in ev_info:
        parameters = ev_info['parameters'] or {}
    else:
        parameters = {}

    # pattern matching makes the case logic MUCH simpler.
    match parameters:
        # TODO: note, both of these cases are for petstore.
        # So maybe move the logic to the petshop client.
        # BUT otoh, the func is indeed imperfect.
        # 'type': 'object',     # NOOOOOOOOOOOOOOOOOOOO!!!!
        # fails when parameters is a list instead of a dict.
        # thus
        # # TODO: figure out what the real problem is.
        # and fix in the appropriate place.
        case [{'name': thing}] if thing=='body':
            print('.....................................yoohoo body GUARD')
            return parameters[0]['schema']
        case [{'name': 'body'}]:   # identical to above and therefore unreachable.
            print('.....................................yoohoo body')
            return parameters[0]['schema']
        case [{'name': 'status'}]:  # {'name': 'status'} is definitely petstore-specific
            print('yoohoo status')
            return parameters[0]

    pr = extract_from_dict_list(parameters, 'required')
    return {
        'required': [key for key in pr if pr[key]],
        'properties': extract_from_dict_list(parameters, 'schema'), 
        'additionalProperties': False, 
        'type': 'object',     # OK
    }
  finally:
    pass

        
def head_func(endpoint, verb):
    return {'user-agent': 'python-httpx/0.27.2'}


class config:
    swagger_path = local.swagger.petstore
    api_base = local.api_base.petstore
    alt_swagger = altered_raw_swagger
    head_func = head_func
    validate = local_validate


api_tools.prep_func = prep_func
api_tools.parameters_to_schema = parameters_to_schema


_validator = dynamic_validator(config)
call = dynamic_call(config)

