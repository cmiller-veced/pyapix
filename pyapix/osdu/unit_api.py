
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
    swagger_path = '~/osdu/service/unit-service/docs/v3/api_spec/unit_service_openapi_v3.json'
    api_base = 'https://yoohoo' 
    alt_swagger = altered_raw_swagger
    head_func = head_func
    validate = local_validate



name = 'Unit'
ends = endpoints_and_verbs(parsed_file_or_url(config.swagger_path))
_validator = dynamic_validator(config)
call = dynamic_call(config)
service = Service(name, call, _validator, ends)


# aaaaaaaaarg!
# Seems impossible to delete this way.
# The only way to delete a buncha stuff then is one at a time.
#
# Solution...
# define service directly here.



# import copy
# #snapshot = copy.deepcopy(globals().items())
# snapshot = list(globals())
# to_delete = []
# #for (name, thing) in snapshot:
# for name in snapshot:
#     if (name not in ['call', '_validator', 'ends']) and not name.startswith('__'):
#         to_delete.append(name)
# #for thing in to_delete: del thing
# for name in globals():
#     if (name not in ['call', '_validator', 'ends']) and not name.startswith('__'):
#         try:
#             del globals()[name]
#         except RuntimeError:
#             print(name)
# 

