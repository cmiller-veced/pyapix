import json
import jsonref
from jsonschema import FormatChecker
import httpx

from tools import (dvalidator, raw_swagger, identity_func,
                   extract_from_dict_list,
                   retry_call,
                   LocalValidationError,
                   )

class ValidDataBadResponse(LocalValidationError): pass

class SurpriseArgs(Exception): pass
class NonDictArgs(SurpriseArgs): pass
class ListArgs(SurpriseArgs): pass


def parameters_to_schema(parameters):
    if len(parameters) == 1 and parameters[0]['name'] == 'body':   # petstore
        return parameters[0]['schema']
    if len(parameters) == 1 and parameters[0]['name'] == 'status':   # petstore
        thing = parameters[0]
#        for key in 'in description collectionFormat required name'.split():
#         for key in 'description collectionFormat required name'.split():
#             if key in thing:
#                 thing.pop(key)
        return thing

    pr = extract_from_dict_list(parameters, 'required')
    globals().update(locals())
    return {
        'required': [key for key in pr if pr[key]],
        'properties': extract_from_dict_list(parameters, 'schema'), 
        'additionalProperties': False, 
        'type': 'object',     # NOOOOOOOOOOOOOOOOOOOO!!!!
    }

def test_2():
    parameters = [{'name': 'status', 'in': 'query', 'description': 'Status values that need to be considered for filter', 'required': True, 'type': 'array', 'items': {'type': 'string', 'enum': ['available', 'pending', 'sold'], 'default': 'available'}, 'collectionFormat': 'multi'}]
    s = parameters_to_schema(parameters)
    globals().update(locals())


def param_func(pdict):
  try:
    """
    Extract info for inserting into schema.
    """
    d = { 'type': pdict['type'], }
    for key in ['required', 'name', 'schema']:
        if key in pdict:
            d[key] = pdict[key]
    if 'schema' not in d:
        d['schema'] = {}
        for key in ['format', 'enum', 'type']:
            if key in pdict:
                d['schema'][key] = pdict[key]
        if d['schema']['type'] == 'file':
            d['schema']['type'] = 'string'
    return d
  finally:
    globals().update(locals())


def test_parameters_to_schema():
  try:
    parameters = [{'description': 'Created user object',
  'in': 'body',
  'name': 'body',
  'required': True,
  'schema': {'properties': {'email': {'type': 'string'},
                            'firstName': {'type': 'string'},
                            'id': {'format': 'int64', 'type': 'integer'},
                            'lastName': {'type': 'string'},
                            'password': {'type': 'string'},
                            'phone': {'type': 'string'},
                            'userStatus': {'description': 'User Status',
                                           'format': 'int32',
                                           'type': 'integer'},
                            'username': {'type': 'string'}},
             'type': 'object',
             'xml': {'name': 'User'}}}]
    schema = parameters_to_schema(parameters)

    endpoint, verb = ('/pet/{petId}/uploadImage', 'post')
    parameters = [{'name': 'petId', 'in': 'path', 'description': 'ID of pet to update', 'required': True, 'type': 'integer', 'format': 'int64'}, {'name': 'additionalMetadata', 'in': 'formData', 'description': 'Additional data to pass to server', 'required': False, 'type': 'string'}, {'name': 'file', 'in': 'formData', 'description': 'file to upload', 'required': False, 'type': 'file'}]
    schema = parameters_to_schema(parameters)

    p2 = [param_func(d) for d in parameters]
    s2 = parameters_to_schema(p2)

  finally:
    globals().update(locals())



def dv(config):
    swagger_path = config.swagger_path
    local_validate = config.validate
    altered_raw_swagger = config.alt_swagger
    def validator(endpoint, verb='get'):
        """Return a validator for `(endpoint, verb)`.
        """
        jdoc = jsonref.loads(json.dumps(raw_swagger(swagger_path)))
        jdoc = altered_raw_swagger(jdoc)
        ev_info = jdoc['paths'][endpoint][verb]
        globals().update(locals())
#        parameters = ev_info['parameters'] or {}
        if 'parameters' in ev_info:
            parameters = ev_info['parameters'] or {}
        else:
            parameters = {}
        globals().update(locals())
        schema = parameters_to_schema(parameters)
        return dvalidator(local_validate)(schema, format_checker=FormatChecker())
    return validator


# TODO: add headers to `prepped`       NO!!!!!!!!
def prep_func(api_base, 
              swagger_path, 
              altered_raw_swagger=identity_func,
              #              headers=None
    ):
#     """
#     headers is a function that accepts (endpoint, verb) and returns header(s) as
#     json/dict.
#     """
    def prepped(endpoint, verb, args):
      try:
        """Prepare args for passing to (endpoint, verb).
        """
        if not args:                                 # diff
            return (api_base + endpoint, verb, {})   # diff

        # NO
        if type(args) is str:                   # diff
#            return (api_base + endpoint, verb, args)   # fails
            raise NonDictArgs(args)      # Should not have this. ????
        # NWS /products/{productId} get with args == 'ZFP'
        # fails.
        # But wait.  Maybe it is simply bad data..

#         if type(args) is not dict:                   # diff
#             raise NonDictArgs(args)

        jdoc = raw_swagger(swagger_path)
        jdoc = jsonref.loads(json.dumps(jdoc))
        rs = altered_raw_swagger(jdoc)   # TODO: must alter AFTER deref.
        paths = rs['paths']
        ev_params = paths[endpoint][verb]['parameters'] or {}
        location = extract_from_dict_list(ev_params, 'in')
        request_params = {}
        query = {}
        if type(args) is list:
            raise ListArgs(args)

        for arg in args:
            plocation = location[arg] if arg in location else 'query'
            if plocation == 'path':
                endpoint = endpoint.replace('{'+arg+'}', str(args[arg]))
            elif plocation == 'query':
                query[arg] = args[arg]
        if query:
            request_params['params'] = query
        return (api_base + endpoint, verb, request_params)
      finally:
        globals().update(locals())
    return prepped



# TODO: add something to add headers to a few random endpoints to illustrate.
# Maybe.
# TODO: no need to test with bad params????????//
# Because those should be caught by validation...


def dcall(config):
    """
    """
    api_base = config.api_base
    swagger_path = config.swagger_path
    head_func = config.head_func
    altered_raw_swagger = config.alt_swagger

    prepped = prep_func(api_base, swagger_path, altered_raw_swagger)
    @retry_call()
    def call(endpoint, verb, params):
        """Call (endpoint, verb) with params.
        """
        heads = head_func(endpoint, verb) if head_func else {}
        (url, verb, request_params) = prepped(endpoint, verb, params)
        request = httpx.Request(verb, url, **request_params, headers=heads)
        # TODO: return headers from `prepped`.
        globals().update(locals())
        with httpx.Client() as client:
            return client.send(request)  
    return call

