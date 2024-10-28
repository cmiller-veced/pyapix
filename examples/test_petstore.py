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

from collections import defaultdict
import json
import jsonref
import jsonschema

from apis.tools import parsed_file_or_url
from apis.api_tools import NonDictArgs, SurpriseArgs
from apis.petstore import _validator, call, config, altered_raw_swagger
from test_data.petstore import test_parameters 

from apis import api_tools
from apis.api_tools import *
from apis.tools import *


# TODO: clarify messaging.
def test_validate_and_call():
  try:
    bad_param_but_ok = defaultdict(list)
    good_param_not_ok = defaultdict(list)
    surprise_args = defaultdict(list)
    jdoc = parsed_file_or_url(config.swagger_path)  # TODO: pass flag for deref vs not.?
    jdoc = jsonref.loads(json.dumps(jdoc))
    paths = altered_raw_swagger(jdoc)['paths']
    for endpoint in paths:
        for verb in paths[endpoint]:

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
#                    break  # after first params

                    if not response.is_success:
                        good_param_not_ok[(endpoint, verb)].append(params)
#                        raise ValidDataBadResponse(params)
                        continue
                    if response.is_success:
                        print('   ok good call')
#                break  # before bad ones
                for params in things[verb]['bad']:
                    assert not validator.is_valid(params)
                    print('   ok bad NOT valid', params)
                    try:
                        response = call(endpoint, verb, params)
                        if response.is_success:
                            bad_param_but_ok[(endpoint, verb)].append(params)
                    except (NonDictArgs, KeyError):
                        continue
#        break  # after first endpoint

  finally:
    bad_param_but_ok = dict(bad_param_but_ok)
    good_param_not_ok = dict(good_param_not_ok)
    globals().update(locals())


def test_pet_sequence():
    # /pet post                OK
    # /pet/{petId} get         OK
    # /pet put                 OK
    # /pet/{petId} get         OK
    # /pet/{petId} post        debugging
    # /pet/{petId} get
    # /pet/{petId} delete      OK
    # /pet/{petId} get         OK
  try:

    N = 4321
    endpoint, verb = '/pet', 'post'
    validator = _validator(endpoint, verb)
    args = {'id': N}
    response = call(endpoint, verb, args)
    assert response.is_success
    assert response.json() == {'id': N, 'photoUrls': [], 'tags': []}
    r1 = response

    endpoint, verb = '/pet/{petId}', 'get'
    args = {'petId': N}
    response = call(endpoint, verb, args)
    assert response.is_success
    assert response.json() == {'id': N, 'photoUrls': [], 'tags': []}
    r2 = response

    endpoint, verb = '/pet', 'put'
    args = {'id': N, 'name': 'kittyX'}
    response = call(endpoint, verb, args)
    assert response.is_success
    assert response.json() == {'id': N, 'name': 'kittyX', 'photoUrls': [], 'tags': []}
    r2a = response

    endpoint, verb = '/pet/{petId}', 'get'
    args = {'petId': N}
    response = call(endpoint, verb, args)
    assert response.is_success
    assert response.json() == {'id': N, 'name': 'kittyX', 'photoUrls': [], 'tags': []}
    r2b = response


    endpoint, verb = '/pet/{petId}', 'post'
#     jdoc = parsed_file_or_url(config.swagger_path)  # TODO: pass flag for deref vs not.?
#     jdoc = jsonref.loads(json.dumps(jdoc))
#     paths = altered_raw_swagger(jdoc)['paths']
#     ev_params = paths[endpoint][verb]['parameters'] or {}
#     locs = dict(petId='path', name='formData', status='formData')
#     evd = {}
#     for d in ev_params:
#         pname = d['name']
#         d['in'] = locs[pname]
#         evd[pname] = d
#     ev_params = list(evd.values())
#     location = extract_from_dict_list(ev_params, 'in')
# 
#     # TODO: fix 415 Unsupported Media Type
#     # TODO: fix 415 Unsupported Media Type
#     # TODO: fix 415 Unsupported Media Type
#     # TODO: fix 415 Unsupported Media Type
#     import apis
#     prepped = prep_func(apis.petstore.config)
#     request_params = prepped(endpoint, verb, args)


    args = {'petId': N, 'name': 'kittyY'}
    response = call(endpoint, verb, args)
    assert response.is_success
    # 415   Unsupported Media Type
#    assert response.json() == {'id': N, 'name': 'kittyY', 'photoUrls': [], 'tags': []}
    assert response.json() == {'code': 200, 'type': 'unknown', 'message': '4321'}
    r2c = response

    endpoint, verb = '/pet/{petId}', 'get'
    args = {'petId': N}
    response = call(endpoint, verb, args)
    assert response.is_success
    assert response.json() == {'id': N, 'name': 'kittyY', 'photoUrls': [], 'tags': []}
    r2d = response


    endpoint, verb = '/pet/{petId}/uploadImage', 'post'
    args = {'petId': N, 'additionalMetadata': 'aaaaaaa', 'file': 'foo.png'}
    response = call(endpoint, verb, args)
    assert response.status_code == 200
    msg = response.json()['message']
    assert msg == 'additionalMetadata: aaaaaaa\nFile uploaded to ./upload, 7 bytes'

    endpoint, verb = '/pet/{petId}', 'get'
    args = {'petId': N}
    response = call(endpoint, verb, args)
    assert response.is_success
    assert response.json() == {'id': N, 'name': 'kittyY', 'photoUrls': [], 'tags': []}
    r5 = response

    endpoint, verb = '/pet/{petId}', 'delete'
    args = {'petId': N}
    response = call(endpoint, verb, args)
    assert response.is_success
    assert response.json() == {'code': 200, 'type': 'unknown', 'message': f'{N}'}
    r3 = response

    endpoint, verb = '/pet/{petId}', 'get'
    args = {'petId': N}
    response = call(endpoint, verb, args)
    assert not response.is_success
    assert response.status_code == 404
    assert response.json() == {'code': 1, 'type': 'error', 'message': 'Pet not found'}
    r4 = response


    # ^^^^^^^^^ That completes the CRUD operations for Pet ^^^^^^^^^^^


    endpoint, verb = '/pet/findByStatus', 'get'
    args = {'status': 'available'}
    response = call(endpoint, verb, args)
    assert response.is_success
    rj = response.json()
    assert type(rj) is list
    assert len(rj) > 1
    assert all(type(x) is dict for x in rj)
 
    # TODO: fix location info, etc for the last two endpoints
    # TODO: fix location info, etc for the last two endpoints

  finally:
#     aendpoint = api_tools.endpoint
#     averb = api_tools.verb 
#     arp = api_tools.request_params
#     print(args)
#     print(aendpoint, averb, arp)
    globals().update(locals())
 
