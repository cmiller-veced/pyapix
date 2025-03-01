from datetime import datetime

from pyapix.tool import api_tools
from pyapix.tool.api_tools import (dynamic_validator, dynamic_call, SurpriseArgs)
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


from pyapix.tool.tools import parsed_file_or_url
from pyapix.tool.api_tools import endpoints_ands_verbs
ends = endpoints_ands_verbs(parsed_file_or_url(config.swagger_path))
_validator = dynamic_validator(config)
call = dynamic_call(config)


# end of the API client
# ############################################################################

import json

from pyapix.tool.api_tools import endpoints_ands_verbs
from pyapix.tool.tools import parsed_file_or_url, list_of_dict_to_dict
from pyapix.tool.working_with_postman import fetch_thing, insert_params
from pyapix.tool.do_postman_osdu import pm_files
import crs_conversion_api as con

one_dict = list_of_dict_to_dict()

# TODO: mv this...
service_parts = ['api', 'crs', 'catalog', 'conversion', 'search', 'storage',
                 'legal'
]

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


# TODO: rename to test_endpoints_ands_verbs    ??????
def test_inspect_swagger():
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


# TODO: mv with func below
def make_endpoint(url, service):
    eps = [e for (e,v) in service.ends]   # all endpoints for swagger
    up = url['path']
    for i, word in enumerate(up):
        if is_version(word):
            svc = up[:i+1]
            endpoint = '/' + '/'.join(up[i+1:])
            # check here to see if swagger endpoint contains version or not.
            # Include the version if it is in the swagger file.
            if endpoint not in eps:
                for e in eps:
                    if e.endswith(endpoint):
                        endpoint = e
    return endpoint


# TODO: (almost) nothing specific to CRS here.
# mv to somewhere
def request_for_service(service):
    def do_pm_request(postman_request):
      try:
        pr = postman_request['request']
        if 'body' in pr:
            ctrb = pr['body']
    #        assert sorted(list(ctrb)) == ['mode', 'options', 'raw']
            if ctrb['mode'] == 'raw':
                bdecoded = json.loads(ctrb['raw'])
        else:
            bdecoded = ''

        url = pr['url']
        params = one_dict(url['query']) if 'query' in url else {}
        if bdecoded:
            params['body'] = bdecoded

        endpoint = make_endpoint(pr['url'], service)
        verb = pr['method'].lower()

        # TODO: this stuff is hard-coded.
        # Source will be an Environment.
        # Targets will be anything in parameters or headers.
        dpid = one_dict(pr['header'])['data-partition-id']
        source = dict(data_partition_id='foo..dpi..bar')
        subbed = insert_params(dpid, source)
        # TODO: strategy...
        # serialize params
        # substitute
        # deserialize params

        v = service._validator(endpoint, verb)
        schema = v.v.schema   # in case we want to have a look.
        valid_params = 'OK' if v.is_valid(params) else 'invalid params'
        if is_bad_schema(schema):
            valid_params = 'crap schema'
            assert endpoint, verb == ('/coordinate-reference-system', 'get')
            # TODO: this (endpoint, verb) has no useful schema.
            # What to do about it?
        # TODO: call the endpoint with the params.

        print(postman_request['name'])
        print(endpoint, verb)
        print('params', params)
        print('............', valid_params)
        print()
      finally:
        globals().update(locals())
    return do_pm_request


# TODO: mv  (to api_tools?)
class Service:
    def __init__(self, call, _validator, ends):
        self.call = call
        self._validator = _validator
        self.ends = ends

smap = {
    'CRS Catalog': Service(call, _validator, ends),
    'CRS Conversion': Service(con.call, con._validator, con.ends),
}


def test_crs_catalog():   # and conversion too.
    global pmjdoc
    pmjdoc = parsed_file_or_url(pm_files()[0])

    names = ['Core Services', 'CRS Catalog', 'V3']
    print(names[1])
    test_pm_section(pmjdoc, *names)
    print()
    print('+'*77)

    print()
    print(names[1])
    names = ['Core Services', 'CRS Conversion', 'V3', 'v3', 'convertTrajectory']
    names = ['Core Services', 'CRS Conversion', 'V3', 'v3', 'convert']
    test_pm_section(pmjdoc, *names)


# TODO: mv to ?
def test_pm_section(pmjdoc, *names):
  try:
    """
    Grab arbitrary section from Postman file and do the PM requests.
    """
    postman_item = fetch_thing(pmjdoc, *names)
    rnames = [thing['name'] for thing in postman_item['item']]
    service = smap[names[1]]
    do_pm_request = request_for_service(service)
    for name in rnames:
        noms = names + (name,)
        rf = do_pm_request(fetch_thing(pmjdoc, *noms))
  finally:
    globals().update(locals())


"""
enames = ['Core Services', 'Entitlements']   # good output
# show_contents(pmjdoc, *enames)   # good output

>>> ebnames = ['Core Services', 'CRS Catalog', 'Entitlements']
TODO:  weird things happen with this input.  fix.
>>> show_contents(pmjdoc, *ebnames)
Core Services
    CRS Catalog
        Entitlements
            i V3
            r Health Check
>>> show_contents(pmjdoc, 'Core Services', 'CRS Catalog')
Core Services
    CRS Catalog
        i V3
        r Health Check
"""
# TODO: mv to where fetch_thing is.
def show_contents(pmjdoc, *names):
    """
    show_contents(pmjdoc)
    show_contents(pmjdoc, 'Core Services')
    show_contents(pmjdoc, 'Core Services', 'Entitlements')
    show_contents(pmjdoc, 'Core Services', 'CRS Catalog', 'V3')
    """
    pm_item = fetch_thing(pmjdoc, *names)
    space = ' '
    i = 0
    indent = space * i
    for name in names:
        print(f'{indent}{name}')
        i += 4
        indent = space * i
    if 'item' in pm_item:
        for dct in pm_item['item']:
            t = 'r' if 'request' in dct else 'i' 
            print(f"{indent}{t} {dct['name']}")


