from info import local
from nother import dv, dcall


class config:
    swagger_path = local.swagger.libre
    api_base = local.api_base.libre
    alt_swagger = lambda x:x
    head_func = lambda endpoint, verb: {'accept': 'application/json'}
    validate = lambda params: None


_validator = dv(config)
call = dcall(config)


# test
# ############################################################################
from pprint import pprint
from collections import defaultdict
import json
import jsonref     # cross platform
from jsonschema import (validate, FormatChecker,)
from tools import (raw_swagger, ValidDataBadResponse)
import nother
from nother import NonDictArgs
from test_data_libre import test_parameters


def _validate_and_call():
  try:
    bad_param_but_ok = defaultdict(list)
    good_param_not_ok = defaultdict(list)
    jdoc = raw_swagger(config.swagger_path)
    jdoc = jsonref.loads(json.dumps(jdoc))
    paths = config.alt_swagger(jdoc)['paths']
    for endpoint in paths:
        for verb in paths[endpoint]:
            assert verb in 'get post'
            validator = _validator(endpoint, verb)
            print(endpoint, verb)
            if endpoint in test_parameters:
                things = test_parameters[endpoint]
                for params in things['good']:
                    if not validator.is_valid(params):
                        validator.validate(params)
                    print('   ok good valid', params)
                    response = call(endpoint, verb, params)
                    if not response.is_success:
                        # good_param_not_ok[(endpoint, verb)].append(params)
                        good_param_not_ok[(endpoint, verb)].append((params,
                                                                    response.text))
#                        raise ValidDataBadResponse(params)
                        # TODO: why the bad response !!!!!!!!!??????????
                        # TODO: why the bad response !!!!!!!!!??????????
                        # I want to sort this out because libre uses multiple
                        # verbs.
                        # TODO: why the bad response !!!!!!!!!??????????
                        # TODO: why the bad response !!!!!!!!!??????????
                    if response.is_success:
                        print('   ok good call')
                for params in things['bad']:
                    assert not validator.is_valid(params)
                    print('   ok bad NOT valid', params)
                    try:
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
    _validate_and_call()


# head = {'accept': 'application/json'}  # 
# api_file_path = local.swagger.libre
# api_base = local.api_base.libre
# 
# 
# def validate_and_call():
#   try:
#     rs = raw_swagger(api_file_path)       # 
#     with httpx.Client(base_url=api_base) as client:   # 
#         verb_map = dict(get=client.get, post=client.post)
#         for ep in rs['paths']:
# #            print(ep)
#             ep_info = rs['paths'][ep]
#             print(ep, list(ep_info.keys()))
#             ep0 = ep
#             is_valid = validator_func(api_file_path, ep)
# #            print('     ', is_valid.schema)
#             if ep in test_parameters:
#                 things = test_parameters[ep]
#                 if ep0 != ep:
#                     print('   calling .............', ep)
#                 for params in things['good']:
#                     assert is_valid(params)
#                     print('   ok good valid', params)
#                     fetch = verb_map[list(ep_info.keys())[0]]
#                     r = fetch(ep, params=params, headers=head)
#                     assert r.status_code == 200
#                     # running locally
# 
#                     rj = r.json()
#                 for params in things['bad']:
#                     assert is_valid(params)  # TODO: fix
#                     assert is_valid(params)  # TODO: fix
#                     assert is_valid(params)  # TODO: fix
#                     print('   grrr bad but VALID', params)
#                     r = client.get(ep, params=params)
#                     assert r.status_code != 404    # Bad endpoint
#                     assert r.status_code in [400, 500]    # Bad Parameter
#   finally:
#     globals().update(locals())
# 
# 
#if __name__ == '__main__': validate_and_call()

# from jinja2 import Environment, select_autoescape 
# # TODO: remove in favor of newer thing.
# # endpoint_QUERY_params
# def insert_endpoint_params(endpoint, parameters):
#     if not '{' in endpoint:
#         return endpoint
#     env = Environment(autoescape=select_autoescape())
#     template = env.from_string(templatified(endpoint))
#     return template.render(**parameters)
# 
# 
# head = {'accept': 'application/json'}  # 
# api_file_path = local.swagger.libre
# api_base = local.api_base.libre
# 
# 
# 
# def schema_trans(schema_list):
#     d = {}
#     for thing in schema_list:
#         d['name'] = thing['schema'] if 'schema' in thing else {}
#     return {'properties': d}
# 
# 
# def validator_func(openapi_file, endpoint):
#   try:
#     """Return a function to validata parameters for `endpoint`.
#     """
#     rs = raw_swagger(openapi_file)     # protein vs nws vs libre
#     with_refs = jsonref.loads(json.dumps(rs))
#     thing = with_refs['paths'][endpoint]
#     assert len(thing.keys()) == 1
#     verb = list(thing.keys())[0]
#     tv = thing[verb]
#     if 'parameters' in tv:
#         vinfo = tv['parameters']
#     else:
#         vinfo = {}
#     schema = schema_trans(vinfo)     # 
#     assert list(schema.keys()) == ['properties']
# #    print(endpoint, list(schema['properties'].keys()))
#     is_valid = lambda ob: Draft7Validator(schema, format_checker=FormatChecker()).is_valid(ob)
#     return is_valid
#   finally:
#     globals().update(locals())
#     is_valid.endpoint = endpoint
#     is_valid.schema = schema
# 
# 
