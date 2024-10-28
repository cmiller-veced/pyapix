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
from types import SimpleNamespace
import time
import jsonschema
from jsonschema import FormatChecker
from apis.tools import *


class info:
  class local:
    class swagger:
        petstore = '~/local/petstore/swagger.json'
        nws = '~/local/nws/openapi.json'
        worms =  '~/local/worms/openapi.yaml'
  class remote:
    class swagger:
        petstore = 'https://petstore.swagger.io/v2/swagger.json'
        nws = 'https://api.weather.gov/openapi.json'


def test_dvalidator(): 

    local_validate = lambda params: None
    schema = {'required': ['ScientificName'], 'properties': {'ScientificName': {'type': 'string'}, 'like': {'type': 'boolean', 'default': 'true'}, 'marine_only': {'type': 'boolean', 'default': 'true'}, 'offset': {'type': 'integer', 'default': 1}}, 'additionalProperties': False, 'type': 'object'}
    validator = dvalidator(local_validate)(schema, format_checker=FormatChecker())

    params = {'ScientificName': 'Solea solea'}
    assert validator.is_valid(params) is True
    assert validator.validate(params) is None

    params = {'taxonid': 127160}
    assert validator.is_valid(params) is False
    with pytest.raises(jsonschema.exceptions.ValidationError):
        validator.validate(params)

    params = {}
    assert validator.is_valid(params) is False
    with pytest.raises(jsonschema.exceptions.ValidationError):
        validator.validate(params)


def test_retry():

    @retry_call()
    def fun(url, verb, request_params):
        return SimpleNamespace(is_success=True)

    tr = fun(0, 0, 0)
    assert tr.is_success is True

    @retry_call(n=2)
    def fun(url, verb, request_params):
        return SimpleNamespace(is_success=False)

    t0 = time.time()
    tr = fun(0, 0, 0)
    td = time.time() - t0
    assert tr.is_success is False
    assert 3 < td < 3.1


def test_loading():
    foo = dict(local=info.local, remote=info.remote)
    for key in foo:
        print(key)
        thing = foo[key]
        dct = dict(thing.swagger.__dict__)
        keys = [k for k in dct if not k.startswith('__')]
        for key in keys:
            jdoc = parsed_file_or_url(dct[key])
            assert type(jdoc) is dict
            assert len(jdoc) > 3
            print(key, len(jdoc))
        print()


def test_extract_from_dict_list():
    dlist = [
        dict(name='first', a=1, b=2),
        dict(name='second', a=3, b=4),
        dict(name='third', a=5, b=6, c=7),
    ]
    foo = extract_from_dict_list(dlist, 'a')
    assert foo == {'first': 1, 'second': 3, 'third': 5}
    
    foo = extract_from_dict_list(dlist, 'b')
    assert foo == {'first': 2, 'second': 4, 'third': 6}
    
    foo = extract_from_dict_list(dlist, 'c')
    assert foo == {'third': 7}
    
    foo = extract_from_dict_list(dlist, 'd')
    assert foo == {}
    
    foo = extract_from_dict_list({}, 'd')
    assert foo == {}

    d = dict(e=8)
    with pytest.raises(TypeError):
        extract_from_dict_list(d, 'e')
    
    with pytest.raises(KeyError):
        extract_from_dict_list([d], 'e')
 

def test_raw_file_or_url():
    pet_local = raw_file_or_url(info.local.swagger.petstore)
    pet_remote = raw_file_or_url(info.remote.swagger.petstore)
    ll = len(pet_local)
    lr = len(pet_remote)

    nws_local = raw_file_or_url(info.local.swagger.nws)
    nws_remote = raw_file_or_url(info.remote.swagger.nws)
    ll = len(nws_local)
    lr = len(nws_remote)


def test_parsed_file_or_url():
    pet_local = parsed_file_or_url(info.local.swagger.petstore)
    pet_remote = parsed_file_or_url(info.remote.swagger.petstore)
    assert list(pet_local) == list(pet_remote)

    nws_local = parsed_file_or_url(info.local.swagger.nws)
    nws_remote = parsed_file_or_url(info.remote.swagger.nws)
    assert list(nws_local) == list(nws_remote)
    assert list(nws_local['paths']) == list(nws_remote['paths'])


def xtest_toml():
    import tomllib    # requires 3.11
    tpath = 'foo.toml'
    with open(tpath) as fh:
        ts = fh.read()
    tdoc = tomllib.loads(ts)
    # TODO: note, this is more of a demo than a test.
    # Prep for using toml.

