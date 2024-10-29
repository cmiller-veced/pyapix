from apis.tools import (raw_swagger, LocalValidationError,)
from apis.api_tools import (dynamic_validator, dynamic_call,)

from info import local

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



