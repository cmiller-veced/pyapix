from datetime import datetime

from .api_tools import (dynamic_validator, dynamic_call, SurpriseArgs)
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
        if d['schema']['type'] == 'file':
            d['schema']['type'] = 'string'
#    if list(d['properties']) == ['body']
    return d
  finally:
    globals().update(locals())


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
#         assert 'get' in epdoc
#         assert 'parameters' in epdoc['get']
#         if 'parameters' in epdoc:
#             eprams = epdoc.pop('parameters')
#             jdoc['paths'][endpoint]['get']['parameters'].extend(eprams)
    return jdoc
  finally:

    globals().update(locals())
#    vsch = {d['name']: param_func(d) for d in vpam}
    globals().update(locals())

        
def head_func(endpoint, verb):
    return {'user-agent': 'python-httpx/0.27.2'}


class config:
    swagger_path = local.swagger.petstore
    api_base = local.api_base.petstore
    alt_swagger = altered_raw_swagger
    head_func = head_func
    validate = local_validate


_validator = dynamic_validator(config)
call = dynamic_call(config)



