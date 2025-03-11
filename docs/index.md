# pyapiX:  Python clients for REST APIs

## Overview

`pyapiX`  includes Python clients for several REST APIs with the purpose of
demonstrating the power of the approach.  
The clients are low-level, making no
assumptions about how the data will be used, but instead favoring minimal
intervention.  

Endpoints are called by passing the endpoint name and verb, as
presented in SwaggerUI, along with a dictionary of parameters.  `pyapiX`  takes
care of passing the parameters correctly to the API.
Each endpoint call returns the raw `httpx` object.

Validation is optional.

All pertinent information comes from the OpenAPI/Swagger file.

## Installation

    uv pip install pyapix
    or
    pip install pyapix


## Testing

    git clone https://github.com/cmiller-veced/pyapix.git
    cd pyapix/pyapix/test
    pytest .
    or
    pytest test_nws.py


## Viewing the documentation locally

    uv pip install mkdocs
    cd pyapix/docs
    mkdocs serve
    # point browser to http://127.0.0.1:8000/


