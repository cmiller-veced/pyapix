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

try:
    from pyapix.tool.tools import parsed_file_or_url
    from pyapix.tool.api_tools import NonDictArgs, SurpriseArgs
    from pyapix.client import petstore as petstore_api
    from pyapix.client.petstore import _validator, call, config, altered_raw_swagger
except:
    from pyapix.apis.tools import parsed_file_or_url
    from pyapix.apis.api_tools import NonDictArgs, SurpriseArgs
    from pyapix.apis import petstore as petstore_api
    from pyapix.apis.petstore import _validator, call, config, altered_raw_swagger


try:
    from pyapix.tool.peemish import run_seq, sequence_creator
    from pyapix.apis.peemish import run_seq, sequence_creator
except:
    exec(open('../tool/peemish.py').read())

test_data_file = '../test_data/petstore_data.yaml'
pet_sequence_file = '../test_data/pet_sequence.yaml'
petstore_data = parsed_file_or_url(test_data_file)
sequence_data = parsed_file_or_url(pet_sequence_file)


def test_validate_and_call():
  try:
    test_parameters = petstore_data['test_parameters']
    bad_param_but_ok = defaultdict(list)
    good_param_not_ok = defaultdict(list)
    surprise_args = defaultdict(list)
    jdoc = parsed_file_or_url(config.swagger_path) #TODO:flag for deref vs not.?
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


def test_seq(name=None):
    create_sequence = sequence_creator(petstore_api, sequence_data)
    snames = [name] if name else ['pet_other_sequence', 'pet_crud_sequence']
    run_seq([create_sequence(sequence_data[sn]) for sn in snames])

