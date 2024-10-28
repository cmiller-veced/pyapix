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

import pytest
import httpx

from apis import api_tools
from apis.api_tools import (
    parameters_to_schema, 
    dynamic_call, 
    dynamic_validator,
    prep_func,
    BadEndpointOrVerb,
)
import apis
import apis.petstore


def test_dvalidator(): 
    print('test_dvalidator')
    # test using worms API
    class config:
        swagger_path = '~/local/worms/openapi.yaml'
        alt_swagger = lambda x: x 
        validate = lambda params: None

    dv = dynamic_validator(config)

    with pytest.raises(BadEndpointOrVerb):
        endpoint, verb = 'foo', 'get'
        dv(endpoint, verb)
    with pytest.raises(BadEndpointOrVerb):
        endpoint, verb = '/AphiaClassificationByAphiaID/{ID}', 'foo'
        dv(endpoint, verb)

    endpoint, verb = '/AphiaClassificationByAphiaID/{ID}', 'get'
    validator = dv(endpoint, verb)
    assert validator.is_valid({'ID': 127160})
    assert not validator.is_valid({'id': 127160})

    endpoint, verb = '/AphiaRecordsByName/{ScientificName}', 'get'
    validator = dv(endpoint, verb)
    assert validator.is_valid({'ScientificName': 'Solea solea'})
    assert not validator.is_valid({'taxonid': 0})

    # test using petstore API
    class config:
        swagger_path = '~/local/petstore/swagger.json'
        alt_swagger = lambda x: x 
        validate = lambda params: None
        api_base = 'petstore'

    import apis
    import apis.petstore
    dv = apis.petstore.dynamic_validator(config)

    endpoint, verb = '/pet/findByStatus', 'get'
    validator = dv(endpoint, verb)
    args = dict(status= ['sold', 'pending'])
    args = ['sold', 'pending']
    globals().update(locals())
    validator.validate(args)
    assert validator.is_valid(args)
    print('end test_dvalidator')


def param_func(pdict):
  try:
    d = {}
    for key in ['required', 'name', 'schema']:
        if key in pdict:
            d[key] = pdict[key]
    if 'schema' not in d:
        d['schema'] = {}
        for key in ['format', 'enum', 'type', 'items', 'default']:
            if key in pdict:
                d['schema'][key] = pdict[key]
    return d
  finally:
    globals().update(locals())


def altered_raw_swagger_petstore(jdoc):
    for endpoint in jdoc['paths']:
        for verb in jdoc['paths'][endpoint]:
            parameters = jdoc['paths'][endpoint][verb]['parameters']
            assert type(parameters) is list
            assert all(type(thing) is dict for thing in parameters)
            jdoc['paths'][endpoint][verb]['parameters'] = [param_func(d) for d in parameters]
    return jdoc


def test_prep_func(): 
  try:
    print('################################### start test_prep_func')
    # test using worms API
    class config:
        swagger_path = '~/local/worms/openapi.yaml'
        alt_swagger = lambda x: x 
        api_base = ''
        head_func = lambda *pos, **kw: {}

    pd = prep_func(config)

    endpoint, verb = '/AphiaClassificationByAphiaID/{ID}', 'get'
    args = {'ID': 127160}
    (u, v, request_params) = pd(endpoint, verb, args)
    assert u.endswith('/AphiaClassificationByAphiaID/127160')
#    assert request_params == {}
    # OK

    # test using petstore API
    class config:
        swagger_path = '~/local/petstore/swagger.json'
        alt_swagger = lambda x: x 
        validate = lambda params: None
        api_base = 'https://petstore.swagger.io/v2'
        head_func = lambda *pos, **kw: {}

    pd = apis.petstore.prep_func(config)

    uploadImage = False
    uploadImage = True
    endpoint, verb = '/pet/{petId}/uploadImage', 'post'
    print(endpoint, verb)
    if uploadImage:
        args = {'petId': 1234}
        print('  ', args)
        (u, v, request_params) = pd(endpoint, verb, args)
        assert u.endswith('/pet/1234/uploadImage')
        assert request_params == {}
        # OK
        # check if the request works...
        dc = dynamic_call(config)
        response = dc(endpoint, verb, args)
        assert response.status_code == 415
        assert response.reason_phrase == 'Unsupported Media Type'  # because we sent nothing.
        # OK
        print('  ', 'OK')

    if uploadImage:
        args = {'petId': 1234, 'additionalMetadata': 'aaaaaaa', 'file': 'foo.png'}
        print('  ', args)
        (u, v, request_params) = pd(endpoint, verb, args)
        assert u.endswith('/pet/1234/uploadImage')
        assert request_params == {'data': {'additionalMetadata': 'aaaaaaa'}, 'files': {'file': 'foo.png'}}

        # check if the request works...
        dc = dynamic_call(config)
        response = dc(endpoint, verb, args)
        assert response.status_code == 200
        assert response.json()['message'] == 'additionalMetadata: aaaaaaa\nFile uploaded to ./upload, 7 bytes'
        # OK
        print('  ', 'OK')


    biggie = False
    biggie = True
    if biggie:

        endpoint, verb = '/pet', 'post'
        print(endpoint, verb)
        args = {'id': 1234, 'category': {}, 'name': 'fluff', 'photoUrls': [], 'status': 'available', 'tags': []}
        print('  ', args)
        (u, v, request_params) = pd(endpoint, verb, args)
        assert request_params == {'json': args}
        # TODO: this one also seems fishy ???????
        assert list(request_params) == ['json']
        print(endpoint, verb)
        print('  args', args)
        print('  prep', request_params)
        print()
        # INVESTIGATE

        # checking if the request works...
        dc = dynamic_call(config)
        response = dc(endpoint, verb, args)
        assert response.status_code == 200
    #    assert response.json() == args
        post_response = response
        post_args = args

        # a GET request to verify the resource was created.
        endpoint, verb = '/pet/{petId}', 'get'
        args = {'petId': 1234}
        (u, v, request_params) = pd(endpoint, verb, args)
        response = dc(endpoint, verb, args)
        assert response.status_code == 200
        get_response = response

        assert post_response.json() == get_response.json()
        assert get_response.json()['name'] == 'fluff'
        print('   OK')
        # OK

        endpoint, verb = '/pet', 'put'
        args = {'id': 1234, 'name': 'buff'}
        (u, v, request_params) = pd(endpoint, verb, args)
        assert request_params == {'json': args}
        print(endpoint, verb)
        print('  args', args)
        print('  prep', request_params)
        print()
        # INVESTIGATE

        response = dc(endpoint, verb, args)
        assert response.status_code == 200
        assert response.json() == {'id': 1234, 'name': 'buff', 'photoUrls': [], 'tags': []}
        put_response = response
        print('   OK')
        # OK

        # GET request to verify the resource was altered.
        endpoint, verb = '/pet/{petId}', 'get'
        args = {'petId': 1234}
        (u, v, request_params) = pd(endpoint, verb, args)
        response = dc(endpoint, verb, args)
        assert response.status_code == 200
        get_response2 = response
        assert put_response.json() == get_response2.json()
        assert get_response2.json()['name'] == 'buff'
        print('   OK')
        # OK

        endpoint, verb = '/pet/{petId}', 'delete'
        args = {'petId': 1234, 'api_key': 'special-key'}
        (u, v, request_params) = pd(endpoint, verb, args)
        assert request_params == {'headers': {'api_key': 'special-key'}}

        # The resource is deleted, without sending the api_key.
        # BUT
        # This should be changed in prep_func.

        print(endpoint, verb)
        print('  args', args)
        print('  prep', request_params)
        request = httpx.Request(v, u, **request_params)
        dc = dynamic_call(config)
        response = dc(endpoint, verb, args)
        delete_response = response
        assert response.status_code == 200
        assert delete_response.json() == {'code': 200, 'type': 'unknown', 'message': '1234'}
        print('   OK')
        # OK

        # GET request to verify the resource was deleted.
        endpoint, verb = '/pet/{petId}', 'get'
        args = {'petId': 1234}
        (u, v, request_params) = pd(endpoint, verb, args)
        response = dc(endpoint, verb, args)
        assert response.status_code == 404
        assert response.reason_phrase == 'Not Found'
        get_response3 = response
        # OK


    endpoint, verb = '/pet/{petId}', 'delete'
    args = {'petId': 1234, 'api_key': 'special-key'}
    (u, v, request_params) = pd(endpoint, verb, args)


    endpoint, verb = '/pet/findByStatus', 'get'
    args = {'status': ['sold', 'pending']}

    (u, v, request_params) = pd(endpoint, verb, args)
    print(endpoint, verb)
    print('  args', args)
    print('  prep', request_params)
    print()

    request = httpx.Request(v, u, **request_params)
    assert str(request.url).endswith('/findByStatus?status=sold&status=pending')

    dc = dynamic_call(config)
    response = dc(endpoint, verb, args)
    rj = response.json()
    assert response.is_success
    assert len(rj) > 1
    # OK

    print('############################################# end test_prep_func')
  finally:
    globals().update(locals())


def test_dynamic_call():
    # TODO: ensure correct petstore config.
    class config:
        swagger_path = '~/local/petstore/swagger.json'
        alt_swagger = lambda x: x 
        validate = lambda params: None
        api_base = 'https://petstore.swagger.io/v2'
        head_func = lambda *pos, **kw: {}

    print('########################################### start test_dynamic_call')
    dc = dynamic_call(config)
    endpoint, verb = '/pet/findByStatus', 'get'
    args = dict(status= ['sold', 'pending'])
    response = dc(endpoint, verb, args)
    print('response', response)
    print('########################################### end test_dynamic_call')


def test_parameters_to_schema():
  try:
    """
    Petstore data
    Verifies function as implemented.  Which is OK, but ...
      could be better.
    """
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
    ev_info = dict(parameters=parameters)
    schema = apis.petstore.parameters_to_schema(ev_info)
#    assert sorted(list(schema)) == ['additionalProperties', 'properties', 'required', 'type']
    assert schema['properties'] == parameters[0]['schema']['properties']

    parameters = [{'name': 'status', 'in': 'query', 'description': 'Status values that need to be considered for filter', 'required': True, 'type': 'array', 'items': {'type': 'string', 'enum': ['available', 'pending', 'sold'], 'default': 'available'}, 'collectionFormat': 'multi'}]
    ev_info = dict(parameters=parameters)
    schema = parameters_to_schema(ev_info)
#    assert schema == {'name': 'status', 'in': 'query', 'description': 'Status values that need to be considered for filter', 'required': True, 'type': 'array', 'items': {'type': 'string', 'enum': ['available', 'pending', 'sold'], 'default': 'available'}, 'collectionFormat': 'multi'}
#    assert schema == parameters[0]

  finally:
    globals().update(locals())


test_parameters_to_schema()
test_dvalidator()
test_prep_func()
test_dynamic_call()

