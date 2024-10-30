from collections import defaultdict

import json
import jsonref

from apis.tools import parsed_file_or_url
from apis.api_tools import NonDictArgs
from apis.obis import _validator, call, config, altered_raw_swagger
from test_data.obis import test_parameters


def test_validate_and_call():
  try:
    bad_param_but_ok = defaultdict(list)
    good_param_not_ok = defaultdict(list)
    jdoc = parsed_file_or_url(config.swagger_path)  # TODO: pass flag for deref vs not.?
    jdoc = jsonref.loads(json.dumps(jdoc))
    paths = altered_raw_swagger(jdoc)['paths']
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
                    except NonDictArgs:
                        break
                    if response.is_success:
                        bad_param_but_ok[(endpoint, verb)].append(params)
  finally:
    bad_param_but_ok = dict(bad_param_but_ok)
    good_param_not_ok = dict(good_param_not_ok)

#     rj = response.json()['results']
#     for r in rj:
#         pass
#     r
#     {'id': 233, 'country': 'Wallis Futuna Islands', 'code': 'WF'}
    globals().update(locals())


#if __name__ == '__main__': validate_and_call()
