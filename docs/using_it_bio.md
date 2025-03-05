## Biological APIs

Many biological databases have REST APIs and `pyapiX` has clients for three of them.

- WoRMS: World Register of Marine Species
- OBIS: xxxxxxx
- Protein Data Bank: xxxxx


### WoRMS

Here is the WoRMS client in action.

    (endpoint, verb) = "/AphiaClassificationByAphiaID/{ID}", "get"
    validator = _validator(endpoint, verb)
    parameters = {"ID": 127160 }
    assert validator.is_valid(parameters)
    response = call(endpoint, verb, parameters)
    assert response.status_code == 200

    (endpoint, verb) = "/AphiaRecordsByName/{ScientificName}", "get"
    validator = _validator(endpoint, verb)
    parameters = {"ScientificName": "Solea solea" }
    assert validator.is_valid(parameters)
    response = call(endpoint, verb, parameters)
    rj = response.json()[0]
    assert rj["kingdom"] == "Animalia"
    assert rj["authority"] == "(Linnaeus, 1758)"

    parameters = {"foo": "Solea solea" }
    assert not validator.is_valid(parameters)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        validator.validate(parameters)


... and now... How to show the validation error?

### OBIS

xxxxx


### Protein Data Bank

pdb


### WoRMS


### OBIS

xxxxx


### Protein Data Bank

pdb
