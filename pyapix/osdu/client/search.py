from pyapix.tool.tools import parsed_file_or_url
from pyapix.tool.api_tools import (dynamic_validator, dynamic_call, endpoints_and_verbs, Service)


class config:
    swagger_path = '~/osdu/service/search-service/docs/api/search_openapi.yaml'
    api_base = 'https://yoohoo' 
    alt_swagger = lambda x:x
    head_func = lambda endpoint, verb: {'user-agent': 'python-httpx/0.27.2'}
    validate = lambda _:None


service = Service(
    'Search', 
    dynamic_call(config), 
    dynamic_validator(config), 
    endpoints_and_verbs(parsed_file_or_url(config.swagger_path)),
)
