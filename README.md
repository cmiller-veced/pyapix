# readme

A tool for quickly creating high quality API clients (SDKs).  Initial target APIs are
those defined in Swagger/OpenAPI.

# How to use it

Show how.  Right here.
If you are familiar with the SwaggerDoc for an API or a Postman collection, the
client will look familiar.  Many of your intuitions from SwaggerDoc or Postman
will help you in working with the client.

    def namespacify(thing):
        from types import SimpleNamespace
        ugly_hack = json.dumps(thing, indent=1)
        return json.loads(ugly_hack, object_hook=lambda d: SimpleNamespace(**d))

    # WoRMS: World Register of Marine Species

    (endpoint, verb) = '/AphiaClassificationByAphiaID/{ID}', 'get'
    validator = _validator(endpoint, verb)
    parameters = {'ID': 127160 }
    assert validator.is_valid(parameters)
    response = call(endpoint, verb, parameters)
    rn = namespacify(response.json())

    assert rn.child.child.child.child.child.child.child.child.child.child.child.child.scientificname == 'Solea solea'
    assert rn.child.child.child.child.child.child.child.child.child.child.child.child.AphiaID == 127160



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



### You

You are familiar with the API.  Are comfortable reading the Swagger Doc
description.  Are comfortable using Postman to access the API.

If you are familiar with either the Swagger Doc or Postman, my code will look
familiar. 
The project takes an approach similar to both of the above.  You get access to
the (endpoint, verb) with the ability to send and recieve data.

