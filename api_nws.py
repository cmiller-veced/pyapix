from datetime import datetime

from info import local
from tools import LocalValidationError
from nother import dv, dcall
# TODO: change some of the `other` names.


class DateOrderError(LocalValidationError): pass


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
    for endpoint in jdoc['paths']:
        epdoc = jdoc['paths'][endpoint]
        assert 'get' in epdoc
        assert 'parameters' in epdoc['get']
        if 'parameters' in epdoc:
            eprams = epdoc.pop('parameters')
            jdoc['paths'][endpoint]['get']['parameters'].extend(eprams)
    return jdoc

        
def head_func(endpoint, verb):
    """nws requires user-agent header.   Returns 403 otherwise.
    """
    return {'user-agent': 'python-httpx/0.27.2'}


class config:
    swagger_path = local.swagger.nws
    api_base = local.api_base.nws
    alt_swagger = altered_raw_swagger
    head_func = head_func
    validate = local_validate


_validator = dv(config)
call = dcall(config)

