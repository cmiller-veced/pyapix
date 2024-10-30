from datetime import datetime

from .tools import ( LocalValidationError,)
from .api_tools import (dynamic_validator, dynamic_call,)
from .info import local

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


_validator = dynamic_validator(config)
call = dynamic_call(config)


