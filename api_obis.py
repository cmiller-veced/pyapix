from datetime import datetime
from info import local
from tools import ( LocalValidationError,)
from nother import (dv, dcall,)


class DateOrderError(LocalValidationError): pass

class ValidDataBadResponse(LocalValidationError): pass


def local_validate(params):
    """Catch data problems missed by the schema.
    # eg start_date > end_date
    params = {
        'start': '2024-09-17T18:39:00+00:00', 
        'end':   '2024-09-18T18:39:00+00:00',
    }
    """
    fmt = '%Y-%m-%dT%H:%M:%S+00:00'
    if 'start' in params and 'end' in params:
        start = params['start']
        end = params['end']
        if datetime.strptime(start, fmt) > datetime.strptime(end, fmt): 
            raise DateOrderError(start, end)


def altered_raw_swagger(jdoc):
    """Alter raw data to conform with local code assumptions.
    This function takes a swagger doc as a json and returns json.
    """
    x = jdoc['components']['parameters']['datasetid']
    jdoc['components']['parameters']['id_dataset'] = x
    return jdoc


class config:
    swagger_path = local.swagger.obis
    api_base = local.api_base.obis
    alt_swagger = altered_raw_swagger
    head_func = lambda endpoint, verb: {}
    validate = local_validate


_validator = dv(config)
call = dcall(config)


# test
# ############################################################################
from pprint import pprint
from collections import defaultdict
from tools import ( raw_swagger, )
import json
import jsonref
import nother
from nother import NonDictArgs
from test_data_obis import test_parameters


def validate_and_call():
  try:
    bad_param_but_ok = defaultdict(list)
    good_param_not_ok = defaultdict(list)
    jdoc = raw_swagger(local.swagger.obis)  # TODO: pass flag for deref vs not.?
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


if __name__ == '__main__':
    validate_and_call()
