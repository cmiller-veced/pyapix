import pytest
from demo_class import validated_for_dict
import types
from pprint import pprint
from types import SimpleNamespace
from collections import defaultdict
from test_data_petstore import test_parameters
import httpx
from jsonschema import ( Draft7Validator, FormatChecker, validate)
from api_petstore import (
    populate_request, 
    endpoint_schema, 
    parameter_list_to_schema, 
    get_schemas, 
    get_endpoint_locations,
)
from tools import local, common


header = {'accept: application/json'}
sample_data = {
    'username': 'merlin', 
    'file': 'foofile', 
    'api_key': 'foobar', 
    'additionalMetadata': 'foof', 
    'name': 'yourName', 
#    'status': 'sold', 
    'status': ['sold'], 
    'password': 'xxxxx', 
    'petId': 99, 
    'orderId': 9, 
    'tags': ['foo']
}


def test_endpoint_locations():
  try:
    jdoc = get_endpoint_locations()['paths']
    for path in jdoc:
        for verb in jdoc[path]:
            assert len(jdoc[path][verb]) == 1
            assert 'parameters' in jdoc[path][verb]
            print(path, verb, jdoc[path][verb]['parameters'])
  finally:
    globals().update(locals())


def test_get_schemas():
  try:
    jdoc = get_schemas()    #['paths']
    assert sorted(list(jdoc)) == ['definitions', 'paths']
    jd = jdoc['definitions']
    jp = jdoc['paths']
    assert list(jd) == ['ApiResponse', 'Category', 'Pet', 'Tag', 'Order', 'User']
    assert list(jp) == ['/pet/{petId}/uploadImage', '/pet', '/pet/findByStatus', '/pet/findByTags', '/pet/{petId}', '/store/inventory', '/store/order', '/store/order/{orderId}', '/user/createWithList', '/user/{username}', '/user/login', '/user/logout', '/user/createWithArray', '/user']
  finally:
    globals().update(locals())


def test_parameter_list_to_schema():
    s = parameter_list_to_schema(es['parameters'])
    validator = Draft7Validator(s, format_checker=FormatChecker())
    x = { 'petId': 1234, }
    assert validator.is_valid(x)



# working
def test_endpoint_schema_validation():
  try:
    """
    """
    endpoint_locations = get_endpoint_locations()['paths']
    # TODO: useit
    jdoc = get_schemas()['paths']
    for endpoint in jdoc:
        if endpoint in ['/pet/{petId}/uploadImage', ]:
            continue
        for verb in jdoc[endpoint]:
            es = endpoint_schema(endpoint, verb)
            loc = endpoint_locations[endpoint][verb]['parameters']

            print(endpoint, verb)
            print(es)
            print('---------------------------------------')
            print(loc)

            validator = Draft7Validator(es, format_checker=FormatChecker())
            samples = test_parameters[endpoint][verb]
            print('---', samples['good'])
            for thing in samples['good']:
                print('---', thing)
                assert validator.is_valid(thing)
                
                # OK.  Now we know it is valid.
                # Hit the endpoint to see if it works.
                (url, request_params) = populate_request(endpoint, verb, thing)
                request = httpx.Request(verb, url, **request_params)
                with httpx.Client(base_url=local.api_base.petstore) as client:   # 
                    response = client.send(request)  
                    assert response.is_success

#                if thing: gthing = thing
            for thing in samples['bad']: 
                assert not validator.is_valid(thing)
            # TODO: call the endpoint with the params
            # need other info from swagger.
            print()
  finally:
    globals().update(locals())


def petstore_validate_and_call1():
  try:
    # TODO: useit
    jdoc = get_schemas()['paths']
    for endpoint in jdoc:
        for verb in jdoc[endpoint]:
            es = endpoint_schema(endpoint, verb)
            print(endpoint, verb)
            print(es)
            validator = Draft7Validator(es, format_checker=FormatChecker())
            samples = test_parameters[endpoint][verb]
            for thing in samples['good']:
                assert validator.is_valid(thing)
                if thing:
                    gthing = thing
            for thing in samples['bad']: 
                assert not validator.is_valid(thing)
    return 
# TODO: useit
# goal:  Make it work like this...
    with httpx.Client(base_url=local.api_base.petstore) as client:   # 
        for endpoint in endpoint_names(rs):
            for verb in endpoint:
                for params in test_data['good']:
                    assert params_ok
                    load_params
                    send_params
                    assert it_worked
                for params in test_data['bad']:
                    assert params_NOT_ok
                    load_params
                    send_params
                    assert NOT_it_worked
  finally:
    pass


def endpoint_info(endpoint, verb):
    """Pull endpoint info relevant for the API call.
    """
    jdoc = get_schemas()['paths']
    for ep in jdoc:
        for v in jdoc[ep]:
            if (endpoint, verb) == (ep, v):
                s = jdoc[endpoint][verb]
    return None


def petstore_endpoint_verbs(endpoint):
    rs = raw_swagger(local.swagger.petstore)
    with_refs = jsonref.loads(json.dumps(rs))
    thing = with_refs['paths'][endpoint]
    return list(thing)


# schema fetching
def get_definition_schemas_petstore():
    rs = raw_swagger(local.swagger.petstore)
    with_refs = jsonref.loads(json.dumps(rs))
    defs = with_refs['definitions']
    assert list(defs) == ['ApiResponse', 'Category', 'Pet', 'Tag', 'Order', 'User']
    return defs
    # The Pet schema is a good one.
    # What a Pet object should conform to.


