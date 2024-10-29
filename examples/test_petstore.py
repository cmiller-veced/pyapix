from collections import defaultdict
import json
import jsonref
import jsonschema

from apis.tools import raw_swagger
from apis.api_tools import NonDictArgs
from apis.petstore import _validator, call, config, altered_raw_swagger

from test_data_petstore import test_parameters 


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
