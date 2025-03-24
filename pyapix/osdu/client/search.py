from pyapix.tool.tools import parsed_file_or_url
from pyapix.tool.api_tools import (dynamic_validator, dynamic_call, endpoints_and_verbs, Service)


class config:
    api_base = 'https://yoohoo' 
    alt_swagger = lambda x:x
    head_func = lambda endpoint, verb: {'user-agent': 'python-httpx/0.27.2'}
    validate = lambda _:None


search = Service(
    'Search', 
    dynamic_call(config), 
    dynamic_validator(config), 
    endpoints_and_verbs(parsed_file_or_url(
        '~/osdu/service/search-service/docs/api/search_openapi.yaml'
    )),
)

notification = Service(
    'Notification', 
    dynamic_call(config), 
    dynamic_validator(config), 
    endpoints_and_verbs(parsed_file_or_url(
       '~/osdu/service/notification/docs/api/notification_openapi.yaml' 
    )),
)

register = Service(
    'Register', 
    dynamic_call(config), 
    dynamic_validator(config), 
    endpoints_and_verbs(parsed_file_or_url(
       '~/osdu/service/register/docs/api/register_openapi.yaml' 
    )),
)

storage = Service(
    'Storage', 
    dynamic_call(config), 
    dynamic_validator(config), 
    endpoints_and_verbs(parsed_file_or_url(
       '~/osdu/service/storage/docs/api/storage_openapi.yaml' 
    )),
)

schema = Service(
    'Schema', 
    dynamic_call(config), 
    dynamic_validator(config), 
    endpoints_and_verbs(parsed_file_or_url(
       '~/osdu/service/schema-service/docs/api/schema_openapi.yaml' 
    )),
)

schema_upgrade = Service(
    'Schema Upgrade', 
    dynamic_call(config), 
    dynamic_validator(config), 
    endpoints_and_verbs(parsed_file_or_url(
       '~/osdu/service/schema-upgrade/docs/openapi.json' 
    )),
)

secret_v1 = Service(
    'Secret V1', 
    dynamic_call(config), 
    dynamic_validator(config), 
    endpoints_and_verbs(parsed_file_or_url(
       '~/osdu/service/secret/docs/api/v1_openapi.json	' 
    )),
)

secret = Service(
    'Secret v2', 
    dynamic_call(config), 
    dynamic_validator(config), 
    endpoints_and_verbs(parsed_file_or_url(
       '~/osdu/service/secret/docs/api/v2_openapi.json' 
    )),
)


