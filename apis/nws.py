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

from .tools import LocalValidationError
from .api_tools import dynamic_validator, dynamic_call
from .info import local


class DateOrderError(LocalValidationError): pass


def local_validate(params):
    """Catch data problems missed by the schema.
    # eg start_date > end_date
    params = {
        'start': '2024-09-17T18:39:00+00:00', 
        'end':   '2024-09-18T18:39:00+00:00',
    }
    """
    fmt = '%Y-%m-%dT%H:%M:%S+00:00'
    if 'start' in params and 'end' in params:
        start = params['start']
        end = params['end']
        if datetime.strptime(start, fmt) > datetime.strptime(end, fmt): 
            raise DateOrderError(start, end)


def altered_raw_swagger(jdoc):
    """Alter raw data to conform with local code assumptions.
    This function takes a swagger doc as a json and returns json.
    """
    for endpoint in jdoc['paths']:
        epdoc = jdoc['paths'][endpoint]
        assert 'get' in epdoc
        assert 'parameters' in epdoc['get']
        if 'parameters' in epdoc:
            eprams = epdoc.pop('parameters')
            jdoc['paths'][endpoint]['get']['parameters'].extend(eprams)
    return jdoc

        
def head_func(endpoint, verb):
    """nws requires user-agent header.   Returns 403 otherwise.
    """
    return {'user-agent': 'python-httpx/0.27.2'}


class config:
    swagger_path = local.swagger.nws
    api_base = local.api_base.nws
    alt_swagger = altered_raw_swagger
    head_func = head_func
    validate = local_validate


_validator = dynamic_validator(config)
call = dynamic_call(config)


# vd = _validator(endpoint, verb)
# vd.is_valid(parameters)
# vd.validate(parameters)
# call(endpoint, verb, parameters)
# The behavior of the two is inconsistent.
# How about this?
# caller = dynamic_call(config) ...
# call = caller(endpoint, verb)
# response = call(parameters)
# I guess that would be called a convenience function?

