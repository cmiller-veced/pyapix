from info import local
from nother import (dv, dcall,)


class config:
    swagger_path = local.swagger.worms
    api_base = local.api_base.worms
    alt_swagger = lambda x: x 
    head_func = lambda endpoint, verb: {}
    validate = lambda params: None


_validator = dv(config)
call = dcall(config)

# MVA.  Minimum Viable API

# test
# ############################################################################
from pprint import pprint
from collections import defaultdict
from tools import ( raw_swagger, )
import json
import jsonref
import nother
from nother import (NonDictArgs, ValidDataBadResponse,)
from test_data_worms import test_parameters


def validate_and_call():
  try:
    bad_param_but_ok = defaultdict(list)
    good_param_not_ok = defaultdict(list)
    jdoc = raw_swagger(config.swagger_path)  # TODO: pass flag for deref vs not.?
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
