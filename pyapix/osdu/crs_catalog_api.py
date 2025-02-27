from datetime import datetime

from pyapix.tool import api_tools
from pyapix.tool.api_tools import (dynamic_validator, dynamic_call, SurpriseArgs)
#from pyapix.tool.api_tools import *
from pyapix.tool.tools import (LocalValidationError, ValidDataBadResponse, )
from pyapix.client.info import local


def local_validate(params):
    return


def altered_raw_swagger(jdoc):
    return jdoc

        
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
import json

from pyapix.tool.tools import parsed_file_or_url, list_of_dict_to_dict
from pyapix.tool.api_tools import endpoints_ands_verbs

from pyapix.tool.working_with_postman import fetch_thing, insert_params
from pyapix.tool.do_postman_osdu import pm_files

# TODO: mv to do_postman_osdu
def is_version(word):
    """
    >>> assert is_version('v3') is True
    >>> assert is_version('v222') is True
    >>> assert is_version('V222') is True
    >>> assert is_version('vx2') is False
    """
    if word[0].lower() == 'v' and word[1:].isdigit():
        return True
    return False


# TODO: mv to do_postman_osdu?    YES
def is_bad_schema(schema):
    if schema == { 'required': [], 'properties': {},
     'additionalProperties': False, 'type': 'object'}:
        return True
    if schema['properties'] == {} and schema['additionalProperties'] == False:
        return True
    return False


one_dict = list_of_dict_to_dict()

service_parts = ['api', 'crs', 'catalog', 'conversion', 'search', 'storage',
                 'legal'
]

# Fill in some missing functionality in tool.tools.

def test_inspect_swagger():
  try:
    """
    CRS Catalog
    Have a look at one of the endpoints from the swagger file.
    """
    jdoc = parsed_file_or_url(config.swagger_path)
    evs = endpoints_ands_verbs(jdoc)[:-1][:1]   # just the first endpoint
    evs = endpoints_ands_verbs(jdoc)[:-1]   # ignore /info
    evs = endpoints_ands_verbs(jdoc)
    for (e, v) in evs:
        print(e, v)
        ev = jdoc['paths'][e][v]
        
    defs = jdoc['definitions']
    point = defs['Point']
    ps = defs['PointsInAOUSearch']
    
    # TODO: leverage examples  in definitions.
  finally:
    globals().update(locals())


def test_crs_catalog():
  try:
    pmjdoc = parsed_file_or_url(pm_files()[0])
    assert fetch_thing(pmjdoc) == pmjdoc

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
        else:
            bdecoded = ''

        # TODO: get endpoint            DONE
        up = url['path']
        for i, word in enumerate(up):
            if is_version(word):
                svc = up[:i+1]
                endpoint = '/' + '/'.join(up[i+1:])
        verb = method.lower()

        v = _validator(endpoint, verb)
        schema = v.v.schema   # in case we want to have a look.

        # TODO:  insert template variables...     DONE
        dpi = one_dict(ctr['header'])['data-partition-id']
        source = dict(data_partition_id='foo..dpi..bar')
        subbed = insert_params(dpi, source)

        # TODO: validate postman data   DONE
        params = one_dict(url['query']) if 'query' in url else {}
        if bdecoded:
            params['body'] = bdecoded
        isvalid = v.is_valid(params)
        if is_bad_schema(schema):
            isvalid = 'crap schema'
            assert endpoint, verb == ('/coordinate-reference-system', 'get')

        print(name)
        print(endpoint, verb)
        print('params', params)
        print('............', isvalid)
        print()
  finally:
    globals().update(locals())

