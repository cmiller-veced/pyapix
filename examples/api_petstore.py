from datetime import datetime
from info import local
from tools import (LocalValidationError, ValidDataBadResponse, )
from nother import dv, dcall, SurpriseArgs


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


_validator = dv(config)
call = dcall(config)


# test
# ############################################################################
from pprint import pprint
from collections import defaultdict
from tools import ( raw_swagger, )
import nother
from nother import NonDictArgs
from test_data_petstore import test_parameters 
import json
import jsonref
import jsonschema


# TODO: clarify messaging.
def validate_and_call():
  try:
    bad_param_but_ok = defaultdict(list)
    good_param_not_ok = defaultdict(list)
    surprise_args = defaultdict(list)
    jdoc = raw_swagger(config.swagger_path)  # TODO: pass flag for deref vs not.?
    jdoc = jsonref.loads(json.dumps(jdoc))
    paths = altered_raw_swagger(jdoc)['paths']
    for endpoint in paths:
        for verb in paths[endpoint]:
#             vdoc = paths[endpoint][verb]
#             vpam = paths[endpoint][verb]['parameters']
#             vsch = {d['name']: param_func(d) for d in vpam}

            validator = _validator(endpoint, verb)
            print(endpoint, verb)
            if endpoint in test_parameters:
                things = test_parameters[endpoint]
                for params in things[verb]['good']:
                    if not validator.is_valid(params):
                        validator.validate(params)

                    print('   ok good valid', params)
                    try:
                        response = call(endpoint, verb, params)
                    except SurpriseArgs as exc:
                        surprise_args[(endpoint, verb)].append(params)
                        continue

                    if not response.is_success:
                        good_param_not_ok[(endpoint, verb)].append(params)
#                        raise ValidDataBadResponse(params)
                        continue
                    if response.is_success:
                        print('   ok good call')
                for params in things[verb]['bad']:
                    assert not validator.is_valid(params)
                    print('   ok bad NOT valid', params)
                    try:
                        # TODO: re-extract prepped args.   ?????
                        # NO.
                        # Maybe.
                        # But first get accustomed to debugging as-is.
                        # Should have better visibility there.
                        response = call(endpoint, verb, params)
                    except NonDictArgs:
                        break
                    if response.is_success:
                        bad_param_but_ok[(endpoint, verb)].append(params)
  finally:
    bad_param_but_ok = dict(bad_param_but_ok)
    good_param_not_ok = dict(good_param_not_ok)
    globals().update(locals())


if __name__ == '__main__':
    validate_and_call()
