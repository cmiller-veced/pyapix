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

from .tools import (LocalValidationError,)
from .api_tools import (dynamic_validator, dynamic_call,)
from .info import local

class ValidDataBadResponse(LocalValidationError): pass

class NonTruthy(LocalValidationError): pass

class InvalidAccessionId(LocalValidationError): pass


def local_validate(params):
    """Catch data problems missed by the schema.
    """
    if not params:
        raise NonTruthy(params)
    if params == {'accession': 'xxxxxxxx'}:
        raise InvalidAccessionId(params)


def altered_raw_swagger(jdoc):
    """Alter raw data to conform with local code assumptions.
    """
    patch = dict(parameters=[])
    jdoc['paths']['/das/s4entry']['get'].update(patch)
    jdoc['paths']['/']['get'].update(patch)
    return jdoc


class config:
    swagger_path = local.swagger.protein
    api_base = local.api_base.protein
    alt_swagger = altered_raw_swagger
    head_func = lambda endpoint, verb: {}
    validate = local_validate


_validator = dynamic_validator(config)
call = dynamic_call(config)



