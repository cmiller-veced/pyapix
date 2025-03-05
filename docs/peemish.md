## Peemish

Truly showing the power of `pyapiX` requires a heavy duty system for lots of API
requests.  To that end, `pyapiX` includes a Postman work-alike.  It does not
*look* like Postman but it does the same job (with some distinct improvements).

### Storing the data


Data is stored in YAML format.


```yaml

pet_other_sequence:
  - endpoint:  /pet/findByStatus
    verb: get
    name: Search by status
    args: {'status': 'available'}

```
