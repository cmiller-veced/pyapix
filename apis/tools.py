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

import time
import json
import os
from types import SimpleNamespace

import yaml
import httpx
from jsonschema import Draft7Validator


class LocalValidationError(Exception): pass

class ValidDataBadResponse(LocalValidationError): pass

class RemoteFileReadException(Exception): pass

def identity_func(x): return x


def extract_from_dict_list(list_of_dict, key):
    return {d['name']: d[key] for d in list_of_dict if key in d}


def retry_call(n=3, tfun=lambda i:i):
    def _retry(func):
        def __retry(url, verb, request_params):
            i = 0
            response = SimpleNamespace(is_success=False)
            while not response.is_success and i < n:
                not_started = False
                try:
                    response = func(url, verb, request_params)
                except (httpx.ReadTimeout, httpx.ConnectTimeout):
                    # TODO: capture exceptions?
                    pass
                i += 1
                time.sleep(tfun(i))
            return response
        return __retry
    return _retry


def raw_remote_file(at_path):
    heads = {'user-agent': 'python-httpx/0.27.2'}
    # TODO: header is required by NWS.
    request = httpx.Request('get', at_path, headers=heads)
    with httpx.Client() as client:
        try:
            response = client.send(request)  
        except httpx.ConnectError as exc:
            raise RemoteFileReadException(*exc.args)
    the_doc = response.text
    if response.status_code != 200:
        raise RemoteFileReadException(the_doc)
    return the_doc


def raw_local_file(at_path):
    with open(os.path.expanduser(at_path)) as fh:
        return fh.read()


def raw_file_or_url(at_path):
    match at_path[:4]:    # structural pattern matching requires python 3.10+
        case 'http':
            return raw_remote_file(at_path)
        case _:
            return raw_local_file(at_path)


def parsed_file_or_url(at_path):
    match at_path[-5:]: 
        case '.json':
            return json.loads(raw_file_or_url(at_path))
        case _:
            return yaml.safe_load(raw_file_or_url(at_path))


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

