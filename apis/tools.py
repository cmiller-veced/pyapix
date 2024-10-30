import time
import json
import os

import yaml
import httpx
from jsonschema import Draft7Validator


class LocalValidationError(Exception): pass

class ValidDataBadResponse(LocalValidationError): pass


def identity_func(x):
    return x


def extract_from_dict_list(list_of_dict, key):
    return {d['name']: d[key] for d in list_of_dict if key in d}


# This works but needs good test.
def retry_call(n=3, tfun=lambda i:i):
    def _retry(func):
        def __retry(url, verb, request_params):
            try:
                response = func(url, verb, request_params)
            except (httpx.ReadTimeout, httpx.ConnectTimeout):
                response = lambda:None         # quick & dirty hack
                response.is_success = False    # quick & dirty hack
            if not response.is_success:   # TODO: make this a func??? to generalize.
                i = 0
                while i < n:
                    i += 1
                    time.sleep(tfun(i))
                    response = func(url, verb, request_params)
            return response
        return __retry
    return _retry
# TODO: this whole retry thing is funky
# this line...
#                    response = func(url, verb, request_params)
# appears twice and that is absurd.


class RemoteFileReadException(Exception): pass


def raw_remote_file(at_path):
    heads = {'user-agent': 'python-httpx/0.27.2'}
    # TODO: header is required by NWS.
    request = httpx.Request('get', at_path, headers=heads)
    with httpx.Client() as client:
        response = client.send(request)  
    the_doc = response.text
    if response.status_code != 200:
        raise RemoteFileReadException(the_doc)
    return the_doc


def raw_local_file(at_path):
    with open(os.path.expanduser(at_path)) as fh:
        return fh.read()


#def raw_file_or_url(at_path):  pass
# TODO: name change  DONE
def parsed_file_or_url(at_path):
    if at_path.startswith('http'):
        the_doc = raw_remote_file(at_path)
    else:
        the_doc = raw_local_file(at_path)
    if at_path.endswith('.json'):
        return json.loads(the_doc)
    return yaml.safe_load(the_doc)


def test_loading():
    local_file1 = '~/local/nws/openapi.json'
    remote_file1 = 'https://api.weather.gov/openapi.json'
    local_file2 = '~/local/worms/openapi.yaml'
    remote_file2 = 'https://www.marinespecies.org/rest/api-docs/openapi.yaml'

    local1 = parsed_file_or_url(local_file1)
    remote1 = parsed_file_or_url(remote_file1)
    local2 = parsed_file_or_url(local_file2)
    remote2 = parsed_file_or_url(remote_file2)
    assert local1 == remote1
    assert list(local2['paths']) == list(remote2['paths'])
    globals().update(locals())

# TODO: deprecate raw_swagger
raw_swagger = parsed_file_or_url    # TODO: something.......


"""
  /Users/cary/ve/apx/lib/python3.9/site-packages/apis/tools.py:105: DeprecationWarning: Subclassing validator classes is not intended to be part of their public API. A future version will make doing so an error, as the behavior of subclasses isn't guaranteed to stay the same between releases of jsonschema. Instead, prefer composition of validators, wrapping them in an object owned entirely by the downstream library.
    class D7V(Draft7Validator):
"""
def dvalidator(local_validate): 
    def local_is_valid(params):
        try:
            local_validate(params)
            return True
        except LocalValidationError:
            return False

#    class D7V(Draft7Validator):
    class D7V(Draft7Validator):
        def is_valid(self, thing):
            if not super().is_valid(thing):
                return False
            return local_is_valid(thing)
        def validate(self, thing):
            super().validate(thing)
            return local_validate(thing)

    return D7V


def dvalidator(local_validate): 
    def local_is_valid(params):
        try:
            local_validate(params)
            return True
        except LocalValidationError:
            return False

    class D7V:
        def __init__(self, *pos, **kw):
            self.v = Draft7Validator(*pos, **kw)
        def is_valid(self, thing):
            if not self.v.is_valid(thing):
                return False
            return local_is_valid(thing)
        def validate(self, thing):
            self.v.validate(thing)
            return local_validate(thing)

    return D7V
'''
Above avoids the DeprecationWarning of the first version.
This still needs good testing.
'''


# step 1 to refactoring this to eliminate the DeprecationWarning is to have
# a test.
# And indeed, the dvalidator is a bit fishy.
# I should be able to find an equally brief alternative.
def test_dvalidator(): 
    class config:
        swagger_path = local.swagger.worms
        api_base = local.api_base.worms
        alt_swagger = lambda x: x 
        head_func = lambda endpoint, verb: {}
        validate = lambda params: None

    _validator = dynamic_validator(config)
    validator = _validator(endpoint, verb)
    return

