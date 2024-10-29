---
[apis]: https://github.com/cmiller-veced/pyapix/tree/main/apis
[examples]: https://github.com/cmiller-veced/pyapix/tree/main/examples

---
# readme

A tool for quickly creating high quality API clients (SDKs).  Initial target APIs are
those defined in Swagger/OpenAPI.

# How to use it

If you are familiar with the SwaggerDoc for an API or a Postman collection, the
client will look familiar.  Many of your intuitions from SwaggerDoc or Postman
will help you in working with the client.

    # WoRMS: World Register of Marine Species
    from apis.worms import _validator, call

    (endpoint, verb) = '/AphiaClassificationByAphiaID/{ID}', 'get'
    validator = _validator(endpoint, verb)
    parameters = {'ID': 127160 }
    assert validator.is_valid(parameters)
    response = call(endpoint, verb, parameters)
    assert response.status_code == 200


    (endpoint, verb) = '/AphiaRecordsByName/{ScientificName}', 'get'
    validator = _validator(endpoint, verb)
    parameters = {'ScientificName': 'Solea solea' }
    assert validator.is_valid(parameters)
    response = call(endpoint, verb, parameters)
    rj = response.json()[0]
    assert rj['kingdom'] == 'Animalia'
    assert rj['authority'] == '(Linnaeus, 1758)'


    parameters = {'foo': 'Solea solea' }
    validator.validate(parameters)

    Traceback (most recent call last):
      ...
    jsonschema.exceptions.ValidationError: 'ScientificName' is a required property

    Failed validating 'required' in schema:
        {'required': ['ScientificName'],
         'properties': {'ScientificName': {'type': 'string'},
                        'like': {'type': 'boolean', 'default': 'true'},
                        'marine_only': {'type': 'boolean', 'default': 'true'},
                        'offset': {'type': 'integer', 'default': 1}},
         'additionalProperties': False,
         'type': 'object'}

    On instance:
        {'foo': 'Solea solea'}


# API Definition

The API definition for the above...

    # WoRMS: World Register of Marine Species

    from apis.api_tools import dynamic_validator, dynamic_call


    class config:
        swagger_path = 'https://www.marinespecies.org/rest/api-docs/openapi.yaml'
        api_base = 'https://www.marinespecies.org/rest'
        alt_swagger = lambda x: x 
        head_func = lambda endpoint, verb: {}
        validate = lambda params: None


    _validator = dynamic_validator(config)
    call = dynamic_call(config)

The API definition is about 15 lines.  Most APIs require more but never over 100
lines.  Bigger APIs benefit more from this approach.  This approach eliminates
the manual effort of object definitions required by a DAO-based approach while
more accurately representing the contents of the OpenAPI file.  It also
eliminates the need for manual documentation by leveraging work
already done by the OpenAPI author.  https://www.marinespecies.org/rest/

See the [apis] directory for more client definitions and the [examples]
directory for usage examples.


### You

You are familiar with the API.  Are comfortable reading the Swagger Doc
description.  Are comfortable using Postman to access the API.
The project takes an approach similar to both of the above.  You get access to
the (endpoint, verb) with the ability to send and receive data.

