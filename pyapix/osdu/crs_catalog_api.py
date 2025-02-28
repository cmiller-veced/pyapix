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


from pyapix.tool.tools import parsed_file_or_url, list_of_dict_to_dict
from pyapix.tool.api_tools import endpoints_ands_verbs
ends = endpoints_ands_verbs(parsed_file_or_url(config.swagger_path))
_validator = dynamic_validator(config)
call = dynamic_call(config)


# end of the API client
# ############################################################################
import json



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
    pass
#    globals().update(locals())


# TODO: enclose in outer function per service.

def request_for_service(service):
    def do_pm_request(postman_request):
      try:
        pr = postman_request['request']
        method = pr['method']
        url = pr['url']

        if 'body' in pr:
            ctrb = pr['body']
    #        assert sorted(list(ctrb)) == ['mode', 'options', 'raw']
            if ctrb['mode'] == 'raw':
                bdecoded = json.loads(ctrb['raw'])
        else:
            bdecoded = ''

        # get (endpoint, verb)
        eps = [e for (e,v) in service.ends]   # all endpoints for swagger
        up = url['path']
        for i, word in enumerate(up):
            if is_version(word):
                svc = up[:i+1]
                endpoint = '/' + '/'.join(up[i+1:])
                # check here to see if swagger endpoint contains version or not.
                # Include the version if it is in the swagger file.
                if endpoint not in eps:
                    # TODO: do something.
                    for e in eps:
                        if e.endswith(endpoint):
                            endpoint = e
            # TODO: above is good but has grow enough to warrant a function.
        verb = method.lower()

        # TODO:  insert template variables...     DONE
        dpid = one_dict(pr['header'])['data-partition-id']
        source = dict(data_partition_id='foo..dpi..bar')
        subbed = insert_params(dpid, source)

        # get params
        params = one_dict(url['query']) if 'query' in url else {}
        if bdecoded:
            params['body'] = bdecoded
        valid_params = '???'

        # TODO: validate postman data   DONE
        v = service._validator(endpoint, verb)
        # TODO: this _validator is hard-coded to CRS Catalog.
        # Do it for arbitrary OSDU service.
        schema = v.v.schema   # in case we want to have a look.

        valid_params = 'OK' if v.is_valid(params) else 'invalid params'
        if is_bad_schema(schema):
            valid_params = 'crap schema'
            assert endpoint, verb == ('/coordinate-reference-system', 'get')
            # TODO: this (endpoint, verb) has no useful schema.
            # What to do about it?

        print(postman_request['name'])
        print(endpoint, verb)
        print('params', params)
        print('............', valid_params)
        print()
      finally:
        globals().update(locals())
    return do_pm_request


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


import crs_conversion_api as con
# the different services are associated with the names below.
# Every list of names is associated with a service.  Not 1:1
# 1:N  service:names

class Service:
    def __init__(self, call, _validator, ends):
        self.call = call
        self._validator = _validator
        self.ends = ends

cat_service = Service(call, _validator, ends)
con_service = Service(con.call, con._validator, con.ends)
smap = {
    'CRS Catalog': cat_service,
    'CRS Conversion': con_service,
}


"""
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

enames = ['Core Services', 'Entitlements']   # good output
# show_contents(pmjdoc, *enames)   # good output

cat_names = ['Core Services', 'CRS Catalog', 'V3']
con_names = ['Core Services', 'CRS Conversion', 'V3', 'v3', 'convertTrajectory']


def test_crs_catalog():
    global pmjdoc
    pmjdoc = parsed_file_or_url(pm_files()[0])

    names = ['Core Services', 'CRS Catalog', 'V3']

    names = ['Core Services', 'CRS Conversion', 'V3', 'v3', 'convertTrajectory']
    names = ['Core Services', 'CRS Conversion', 'V3', 'v3', 'convert']
    # TODO: names[1] maps to the service.

    # Woooooohooooooo!!!!!!!!!!!
    # Woooooohooooooo!!!!!!!!!!!
    # Woooooohooooooo!!!!!!!!!!!
    # Kicks ass !!!!!!!!!!!!!!!!

    test_pm_section(pmjdoc, *names)


def test_pm_section(pmjdoc, *names):
  try:
    """
    Grab arbitrary section from Postman file and do the PM requests.
    # TODO: associate section of Postman file with an API client.
    # So far I have two.
    #
    # TODO: and figure out how to deal with the irritating problem of version
    # prefixed to the url for SOME services.
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

The different services have inconsistent swagger files.

>>> exec(open('crs_catalog_api.py').read());    test_crs_catalog()
Convert a list of points
/convert post
params {'body': {'fromCRS': 'osdu:reference-data--CoordinateReferenceSystem:BoundProjected:EPSG::29193_EPSG::1867:', 'toCRS': 'osdu:reference-data--CoordinateReferenceSystem:Geographic2D:EPSG::4326:', 'points': [{'x': 697339.525, 'y': 7239989.403, 'z': 0}]}}
............ ???

>>> pprint(crs_conversion_api.ends)
[('/v4/convertTrajectory', 'post'),
 ('/v4/convert', 'post'),
 ('/v4/convertGeoJson', 'post'),
 ('/v4/info', 'get')]

>>> pprint(ends)
[('/coordinate-transformation', 'get'),
 ('/coordinate-transformation', 'post'),
 ('/coordinate-reference-system', 'get'),
 ('/coordinate-reference-system', 'post'),
 ('/points-in-aou', 'post'),
 ('/info', 'get')]

^^^^ These two groups come from the respective swagger files.
We see some services include the version and others do not.

# TODO: alter created endpoint to account for swagger diffs


"""

