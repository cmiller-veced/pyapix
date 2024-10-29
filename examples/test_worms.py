
from apis.worms import _validator, call

# MVA.  Minimum Viable API

# test
# ############################################################################

def namespacify(thing):
    from types import SimpleNamespace
    import json
    ugly_hack = json.dumps(thing, indent=1)
    return json.loads(ugly_hack, object_hook=lambda d: SimpleNamespace(**d))

# WoRMS: World Register of Marine Species

(endpoint, verb) = '/AphiaClassificationByAphiaID/{ID}', 'get'
validator = _validator(endpoint, verb)
parameters = {'ID': 127160 }
assert validator.is_valid(parameters)
response = call(endpoint, verb, parameters)
rn = namespacify(response.json())

assert rn.child.child.child.child.child.child.child.child.child.child.child.child.scientificname == 'Solea solea'
assert rn.child.child.child.child.child.child.child.child.child.child.child.child.AphiaID == 127160



#########
(endpoint, verb) = '/AphiaRecordsByName/{ScientificName}', 'get'
validator = _validator(endpoint, verb)
parameters = {'ScientificName': 'Solea solea' }
assert validator.is_valid(parameters)
response = call(endpoint, verb, parameters)
rj = response.json()[0]
assert rj['kingdom'] == 'Animalia'
assert rj['authority'] == '(Linnaeus, 1758)'


parameters = {'foo': 'Solea solea' }
#validator.validate(parameters)

 


from collections import defaultdict
import json
import jsonref

from apis.tools import ( raw_swagger, )
from apis import api_tools
from apis.api_tools import (NonDictArgs, ValidDataBadResponse,)

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


#if __name__ == '__main__': validate_and_call()
