
from datetime import datetime

from pyapix.tool import api_tools
from pyapix.tool.api_tools import (dynamic_validator, dynamic_call, SurpriseArgs)
from pyapix.tool.api_tools import *
from pyapix.tool.tools import (LocalValidationError, ValidDataBadResponse, )
from pyapix.client.info import local


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
    swagger_path = '~/osdu/service/crs-catalog-service/docs/api_spec/crs-catalog-openapi-v3.yaml'
    api_base = 'https://yoohoo' 
    alt_swagger = altered_raw_swagger
    head_func = head_func
    validate = local_validate


_validator = dynamic_validator(config)
call = dynamic_call(config)


# end of the API client
# ############################################################################

from pyapix.tool.tools import parsed_file_or_url
from pyapix.tool.working_with_postman import fetch_thing, insert_params
from pyapix.tool.do_postman_osdu import pm_files
from pyapix.tool import do_postman_osdu
from pyapix.tool.api_tools import endpoints_ands_verbs


# Fill in some missing functionality in api_tools.


def inspect_swagger():
  try:
    """
    CRS Catalog
    Have a look at one of the endpoints from the swagger file.
    """
    jdoc = parsed_file_or_url(config.swagger_path)
    evs = endpoints_ands_verbs(jdoc)[:-1][:1]   # just the first endpoint
    evs = endpoints_ands_verbs(jdoc)[:-1]   # ignore /info
    evs = endpoints_ands_verbs(jdoc)
    #                     /v4/convertTrajectory post
    for (e, v) in evs:
        print(e, v)
        ev = jdoc['paths'][e][v]
        
    defs = jdoc['definitions']
    point = defs['Point']
    ps = defs['PointsInAOUSearch']
#    assert ctr['required'] == ['inputStations', 'method', 'trajectoryCRS', 'unitZ']
    
    # TODO: leverage examples  in definitions.
  finally:
    globals().update(locals())


# TODO: mv to tools.py and generalize
def list_to_dict(list_of_dict):
    k = 'key'
    v = 'value'
    return {d[k]:d[v] for d in list_of_dict}

# TODO: mv to tools.py
def list_of_dict_to_dict(key='key', value='value'):
    def inner(list_of_dict):
        return {d[key]: d[value] for d in list_of_dict}
    return inner
one_dict = list_of_dict_to_dict('key', 'value')


def inspect_postman():
  try:
    """
    """
    pmjdoc = parsed_file_or_url(pm_files()[0])
    x = fetch_thing(pmjdoc)
    assert x == pmjdoc

    names = ['Core Services', 'CRS Catalog', 'V3']
    ct = fetch_thing(pmjdoc, *names)
    rnames = [thing['name'] for thing in ct['item']]
    assert rnames == [
        'Search Coordinate Transformation', 
        'Search Coordinate Transformation 2', 
        'Search Coordinate Transformation 3', 
        'V3 Get coordinate transformations', 
        'Search Coordinate Reference Systems', 
        'Coordinate Reference System', 
        'Check area of use']
    for name in rnames:
        noms = names + [name]
        ct = fetch_thing(pmjdoc, *noms)
        ctr = ct['request']
        method = ctr['method']
        url = ctr['url']
        if 'body' in ctr:
            ctrb = ctr['body']
            assert sorted(list(ctrb)) == ['mode', 'options', 'raw']
            if ctrb['mode'] == 'raw':
                bdecoded = json.loads(ctrb['raw'])
            ctr.pop('body')
        else:
            ctrb = ''
            bdecoded = ''
        for word in 'auth header'.split():
            ctr.pop(word)       # for easier inspection.
        print(name)
        print('body', bdecoded)
        print('url', url)
        if 'query' in url:
            rd = url['query']
            nd = list_to_dict(url['query'])
            nn = one_dict(url['query'])
            assert nd == nn
        print(method)
        # TODO: get endpoint
        # TODO: and then do everything else the test_crs_catalog function is
        # doing.
        # We've already decoded all bodies.
        print()
  finally:
    globals().update(locals())

def test_crs_catalog():
  try:
    endpoint, verb = '/v4/convertTrajectory', 'post'

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

