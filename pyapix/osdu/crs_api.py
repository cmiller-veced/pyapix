
from datetime import datetime

# from . import api_tools
# from .api_tools import (dynamic_validator, dynamic_call, SurpriseArgs)
# from .api_tools import *
# from .tools import (LocalValidationError, ValidDataBadResponse, )
# from .info import local

from pyapix.apis import api_tools
from pyapix.apis.api_tools import (dynamic_validator, dynamic_call, SurpriseArgs)
from pyapix.apis.api_tools import *
from pyapix.apis.tools import (LocalValidationError, ValidDataBadResponse, )
from pyapix.apis.info import local

class Foo(LocalValidationError): pass


def local_validate(params):
    """Catch data problems missed by the schema.
    # eg start_date > end_date
    params = {
        'start': '2024-09-17T18:39:00+00:00', 
        'end':   '2024-09-18T18:39:00+00:00',
    }
    """
    fmt = '%Y-%m-%dT%H:%M:%S+00:00'


def altered_raw_swagger(jdoc):
  try:
    """Alter raw data to conform with local code assumptions.
    This function takes a swagger doc as a json and returns json.
    """
    return jdoc
  finally:
    pass

        
def head_func(endpoint, verb):
    return {'user-agent': 'python-httpx/0.27.2'}


class config:
    swagger_path = '~/osdu/service/crs-conversion-service/docs/v4/api_spec/crs_converter_openapi.json'
    api_base = 'https://yoohoo' 
    alt_swagger = altered_raw_swagger
    head_func = head_func
    validate = local_validate


_validator = dynamic_validator(config)
call = dynamic_call(config)


# end of the API client
# ############################################################################

from pyapix.apis.tools import parsed_file_or_url
from .working_with_postman import fetch_thing, insert_params
from .do_postman_osdu import pm_files

# Fill in some missing functionality in api_tools.


# TODO: mv to api_tools
def endpoints_ands_verbs(jdoc):
    return [(p,v) for p in jdoc['paths'] for v in jdoc['paths'][p]]


def inspect_swagger():
  try:
    """
    CRS Conversion
    Have a look at one of the endpoints from the swagger file.
    """
    jdoc = parsed_file_or_url(config.swagger_path)
    evs = endpoints_ands_verbs(jdoc)[:-1][:1]   # just the first endpoint
    evs = endpoints_ands_verbs(jdoc)
    evs = endpoints_ands_verbs(jdoc)[:-1]   # ignore /v4/info
    #                     /v4/convertTrajectory post
    for (e, v) in evs:
        print(e, v)
        ev = jdoc['paths'][e][v]
        
    defs = jdoc['definitions']
    station = defs['TrajectoryStationInV4']
    ctr = defs['ConvertTrajectoryRequestV4']
    assert ctr['required'] == ['inputStations', 'method', 'trajectoryCRS', 'unitZ']
    
    # NOTE: station has examples
    # TODO: leverage examples
  finally:
    globals().update(locals())


def inspect_postman():
    """
    Pull an endpoint request from the Postman file.
    This matches the endpoint inspected in swagger, above.
    """
    pmjdoc = parsed_file_or_url(pm_files()[0])

    # random example from earlier.
    names = [
        'Dataset',
        'dataset-FileCollection.generic',
        '6c. Download file 3 from S3',
        ]
    cd = fetch_thing(pmjdoc, *names)

    # The relevant example today.
    x = fetch_thing(pmjdoc)
    assert x == pmjdoc
    names = ['Core Services', 'CRS Conversion', 'v3', 'convertTrajectory']
    names += ['Convert trajectory stations']
    ct = fetch_thing(pmjdoc, *names)
    assert ct['name'] == 'Convert trajectory stations'
    ctr = ct['request']
    ctrb = ct['request']['body']
    assert sorted(list(ctrb)) == ['mode', 'options', 'raw']
    if ctrb['mode'] == 'raw':
        bdecoded = json.loads(ctrb['raw'])
    """
    CRS Conversion 2
    i              v3 5
    i                  convertTrajectory 1
                         Convert trajectory stations

    /v4/convertTrajectory
    /v4/convert
    /v4/convertGeoJson
    /v4/info

    Pull data from Postman file.
    """


def test_crs_conversion():
  try:
    """
    Pull data from Postman file.
    """
    pmjdoc = parsed_file_or_url(pm_files()[0])
    # same example from above
    rname = 'Convert trajectory stations'
    names = ['Core Services', 'CRS Conversion', 'v3', 'convertTrajectory', rname]
    ct = fetch_thing(pmjdoc, *names)
    ctu = ct['request']['url']
    ctr = ct['request']['url']['raw']
    ctrb = ct['request']['body']
    if ctrb['mode'] == 'raw':
        json.loads(ctrb['raw'])
        # OK.  Here is test data (body) ready for passing to my api client,
        # for validation only ATM.
    endpoint, verb = '/v4/convertTrajectory', 'post'
    # TODO: how to convert the Postman url into a path like ^
    # Not difficult but have not done it yet

    # v = _validator((endpoint, verb))
    # TODO: NOTE  _validator.__doc__ was helpful here in debugging the line
    # above.
    v = _validator(endpoint, verb)
    params = dict(body={})
    assert not v.is_valid(params)

    # TODO: substitute in template before decoding.
    # DONE
    source = dict(data_partition_id='....dpi.....')
    subbed = insert_params(ctrb['raw'], source)
    good_body = json.loads(subbed)
    params = dict(body=good_body)
    v.validate(params)
    good_body['azimuthReference'] = 1
    assert not v.is_valid(params)
    good_body = json.loads(subbed)
    params = dict(body=good_body)
    v.validate(params)
    good_body['azimuthReference'] = 'TRUE_NORTH'
    v.validate(params)

    schema = v.v.schema   # in case we want to have a look.
    # TODO: celebrate !!!!!!!!!!!!!!!!!!!!
    # yahooooooo!!!!!!!!!!!!!!!
    # This kicks ass!!!!!!!!!!!!
    # or at least is the POC.
    # It shows that asses will be kicked!!!!!!!!!!!
  finally:
    globals().update(locals())

# TODO: 
# iterate over Postman file.
# Find all calls to CRS Conversion.
# For each call, 
#     translate url(PM) to endpoint(pyapiX)
#     grab the parameters
#     validate the parameters
# store the parameters in yaml?
# NOTE:  Lots of services in the current PM file
# CRS Conversion    
# CRS Catalog    
# Unit
# Search
# Dataset
# Storage
# pws   whatever that is... workflow maybe
# Register
# Notification
# Partition
# Schema
# Legal
# Entitlements
# Seismic DMS
# 14 of them


if __name__ == '__main__':
    import doctest
    doctest.testmod()

