
from datetime import datetime

from pyapix.tool import api_tools
from pyapix.tool.api_tools import (dynamic_validator, dynamic_call, SurpriseArgs)
from pyapix.tool.tools import (LocalValidationError, ValidDataBadResponse, )
from pyapix.client.info import local
from pyapix.tool.api_tools import endpoints_and_verbs, Service
from pyapix.tool.tools import parsed_file_or_url


def local_validate(params):
    return


def altered_raw_swagger(jdoc):
    return jdoc

        
def head_func(endpoint, verb):
    return {'user-agent': 'python-httpx/0.27.2'}


class config:
    swagger_path = '~/osdu/service/crs-conversion-service/docs/v4/api_spec/crs_converter_openapi.json'
    api_base = 'https://yoohoo' 
    alt_swagger = altered_raw_swagger
    head_func = head_func
    validate = local_validate


ends = endpoints_and_verbs(parsed_file_or_url(config.swagger_path))
_validator = dynamic_validator(config)
call = dynamic_call(config)
service = Service('CRS Conversion', call, _validator, ends)

