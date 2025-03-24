from pyapix.tool.tools import parsed_file_or_url
from pyapix.tool.api_tools import (dynamic_validator, dynamic_call, endpoints_and_verbs, Service)


class config:
    swagger_path = ''
    api_base = 'https://yoohoo' 
    alt_swagger = lambda x:x
    head_func = lambda endpoint, verb: {'user-agent': 'python-httpx/0.27.2'}
    validate = lambda _:None


def sc(config):
    def service_client(name, swagger_path):
        config.swagger_path = swagger_path
        return Service(name, 
            dynamic_call(config), 
            dynamic_validator(config), 
            endpoints_and_verbs(parsed_file_or_url(config.swagger_path)),
        )
    return service_client


class swagger_path:
    search = '~/osdu/service/search-service/docs/api/search_openapi.yaml'
    notification = '~/osdu/service/notification/docs/api/notification_openapi.yaml' 
    register = '~/osdu/service/register/docs/api/register_openapi.yaml' 
    schema = '~/osdu/service/schema-service/docs/api/schema_openapi.yaml' 
    schema_upgrade = '~/osdu/service/schema-upgrade/docs/openapi.json' 
    secret_v1 = '~/osdu/service/secret/docs/api/v1_openapi.json' 
    secret = '~/osdu/service/secret/docs/api/v2_openapi.json' 

    unit = '~/osdu/service/unit-service/docs/v3/api_spec/unit_service_openapi_v3.json'
    legal = '~/osdu/service/legal/docs/api/legal_openapi.yaml'
    entitlements = '~/osdu/service/entitlements/docs/api/entitlements_openapi.yaml'
    dataset = '~/osdu/service/dataset/docs/dataset.swagger.yaml'
    crs_conversion = '~/osdu/service/crs-conversion-service/docs/v4/api_spec/crs_converter_openapi.json'
    crs_catalog = '~/osdu/service/crs-catalog-service/docs/api_spec/crs-catalog-openapi-v3.yaml'

    storage = '~/osdu/service/storage/docs/api/storage_openapi.yaml' 


service_client = sc(config)
search = service_client('Search', swagger_path.search)
notification = service_client('Notification', swagger_path.notification)
register = service_client('Register', swagger_path.register)
schema = service_client('Schema', swagger_path.schema)
schema_upgrade = service_client('Schema Upgrade', swagger_path.schema_upgrade) 
secret_v1 = service_client('Secret V1', swagger_path.secret_v1)
secret = service_client('Secret', swagger_path.secret)

unit = service_client('Unit', swagger_path.unit)
legal = service_client('Legal', swagger_path.legal)
entitlements = service_client('Entitlements', swagger_path.entitlements)
dataset = service_client('Dataset', swagger_path.dataset)
crs_conversion = service_client('CRS Conversion', swagger_path.crs_conversion)
crs_catalog = service_client('CRS Catalog', swagger_path.crs_catalog)

storage = service_client('Storage', swagger_path.storage)


