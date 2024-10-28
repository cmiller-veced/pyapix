import time
import json
import os
from types import SimpleNamespace

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


def raw_swagger(at_path):
    with open(os.path.expanduser(at_path)) as fh:
        if at_path.endswith('.json'):
            return json.load(fh)
        return yaml.safe_load(fh)


def dvalidator(local_validate): 
    def local_is_valid(params):
        try:
            local_validate(params)
            return True
        except LocalValidationError:
            return False

    class D7V(Draft7Validator):
        def is_valid(self, thing):
            if not super().is_valid(thing):
                return False
            return local_is_valid(thing)
        def validate(self, thing):
            super().validate(thing)
            return local_validate(thing)

    return D7V


