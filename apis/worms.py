from apis.api_tools import dynamic_validator, dynamic_call

from info import local


class config:
    swagger_path = local.swagger.worms
    api_base = local.api_base.worms
    alt_swagger = lambda x: x 
    head_func = lambda endpoint, verb: {}
    validate = lambda params: None


_validator = dynamic_validator(config)
call = dynamic_call(config)
