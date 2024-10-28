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
import jsonschema
import jsonref
import pytest

from apis.tools import parsed_file_or_url
from apis.api_tools import (NonDictArgs, ValidDataBadResponse,)
from apis.worms import _validator, call, config
from test_data.worms import test_parameters

#from apis import api_tools

def test_examples():
    (endpoint, verb) = '/AphiaClassificationByAphiaID/{ID}', 'get'
    validator = _validator(endpoint, verb)
    parameters = {'ID': 127160 }
    assert validator.is_valid(parameters)
    response = call(endpoint, verb, parameters)
    assert response.status_code == 200

    (endpoint, verb) = '/AphiaRecordsByName/{ScientificName}', 'get'
    validator = _validator(endpoint, verb)
    parameters = {'ScientificName': 'Solea solea' }
    assert validator.is_valid(parameters)
    response = call(endpoint, verb, parameters)
    rj = response.json()[0]
    assert rj['kingdom'] == 'Animalia'
    assert rj['authority'] == '(Linnaeus, 1758)'

    parameters = {'foo': 'Solea solea' }
    assert not validator.is_valid(parameters)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        validator.validate(parameters)


def test_validate_and_call():
    bad_param_but_ok = defaultdict(list)
    good_param_not_ok = defaultdict(list)
    jdoc = parsed_file_or_url(config.swagger_path)
    jdoc = jsonref.loads(json.dumps(jdoc))
    paths = config.alt_swagger(jdoc)['paths']
    for endpoint in paths:
        for verb in paths[endpoint]:
            print(endpoint, verb)
            validator = _validator(endpoint, verb)
            if endpoint in test_parameters:
                things = test_parameters[endpoint]
                for params in things['good']:
                    if not validator.is_valid(params):
                        validator.validate(params)

                    print('   ok good valid', params)
                    response = call(endpoint, verb, params)
                    gr = response
                    if not response.is_success:
                        good_param_not_ok[(endpoint, verb)].append(params)
                        raise ValidDataBadResponse(params)
                    if response.is_success:
                        print('   ok good call')
                for params in things['bad']:
                    assert not validator.is_valid(params)
                    print('   ok bad NOT valid', params)
                    try:
                        response = call(endpoint, verb, params)
                    except (NonDictArgs, KeyError):
                        continue
                    if response.is_success:
                        bad_param_but_ok[(endpoint, verb)].append(params)
    bad_param_but_ok = dict(bad_param_but_ok)
    good_param_not_ok = dict(good_param_not_ok)

