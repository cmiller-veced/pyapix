import os
import copy
import json
from jsonschema import Draft7Validator, FormatChecker

from pyapix.tool.exploratory import pop_key
from pyapix.tool.api_tools import BadEndpointOrVerb, Service, endpoints_ands_verbs
from pyapix.tool.tools import parsed_file_or_url, list_of_dict_to_dict

from working_with_postman import (is_request, show_contents, insert_params, 
          fetch_thing, is_bad_schema, make_endpoint, )

import crs_conversion_api as con
import crs_catalog_api as cat
import entitlements_api as entitlements
import legal_api as legal
import unit_api as unit


one_dict = list_of_dict_to_dict()

service_parts = ['api', 'crs', 'catalog', 'conversion', 'search', 'storage',
                 'legal'
]

# iterate over Postman file.                   DONE
# Find all calls to CRS Conversion.            DONE
# For each call, 
#     translate url(PM) to endpoint(pyapiX)    DONE
#     grab the parameters                      DONE
#     validate the parameters                  WIP
# create client for crs/catalog                DONE
#     validate the parameters                  DONE
# store the parameters in yaml? (or PM?)


def pm_files():
    preship_dir = '~/osdu/pre-shipping/R3-M24/AWS-M24'
    paths = []
    dname = 'Core Services'
    fnames = [
        'AWS_OSDUR3M24_CoreServices_Collection.postman_collection.json',
#        'AWS_OSDUR3M24_VersionEndPoints_Collection.postman_collection.json'
    ]
    for fname in fnames:
        fpath = os.path.expanduser(f'{preship_dir}/{dname}/{fname}')
        paths.append(fpath)
#     dname = 'Policy'
#     fname = 'AWS_OSDUR3M24_Policy_Collection.postman_collection.json'
#     fpath = os.path.expanduser(f'{preship_dir}/{dname}/{fname}')
#     paths.append(fpath)
    return paths


# (almost) nothing specific to CRS here.
def request_for_service(service):
    def do_pm_request(postman_request):
      try:
        pr = postman_request['request']
        if 'body' in pr:
            ctrb = pr['body']
    #        assert sorted(list(ctrb)) == ['mode', 'options', 'raw']
            if (ctrb['mode'] == 'raw') and ctrb['raw']:
                bdecoded = json.loads(ctrb['raw'])
            else:
                bdecoded = ''
        else:
            bdecoded = ''

        url = pr['url']
        params = one_dict(url['query']) if 'query' in url else {}
        if bdecoded:
            params['body'] = bdecoded

        endpoint = make_endpoint(pr['url'], service)
        verb = pr['method'].lower()

#         entitlement_params = dict(
#             group_email = 'xxxxx',
#         )
#         params.update(entitlement_params)
#         # TODO: insert path vars

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

        bep = False
        vn = None
        try:
            v = service._validator(endpoint, verb)
        except BadEndpointOrVerb:
            bep = True
            bad_ones = ['/legaltags/', '/api/unit/actuator']
            assert any(endpoint.startswith(bw) for bw in bad_ones)
        if bep:
            valid_params = 'weird endpoint\n'
            valid_params += '>>>>>>>>>>>> ' + endpoint + '\n'
            valid_params += '>>>>>>>>>>>> ' + endpoint + '\n'
        else:
            try:
                # TODO: this is for debugging Unit service validation.
                # It seems many of the endpoints have schemas that are not quite
                # correct.
                # TODO: repair the swagger doc.   ?????  maybe
                # It's a bit of dilemma because the schema contains information
                # that is likely useful but is not quite relevant to the
                # parameters.
                vn = Draft7Validator(v.v.schema['properties']['request'], format_checker=FormatChecker())
            except KeyError:
                pass
            schema = v.v.schema   # in case we want to have a look.
            valid_params = 'OK' if v.is_valid(params) else 'invalid params'
            if vn and (valid_params == 'invalid params'):
                valid_params = 'OKxxxx' if vn.is_valid(params) else 'still invalid'
            if is_bad_schema(schema):
                print('yoohoo bad schema')
                print('yoohoo bad schema')
                print('yoohoo bad schema')
                print('yoohoo bad schema')
                cs = schema
                csp = params
                csep = endpoint
                cv = verb
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
        if name == 'Health Check':
            print('yoohoo', name)
            print('yoohoo', name)
            return
        noms = names + (name,)
        thing = fetch_thing(pmjdoc, *noms)
        if is_request(thing):
            print('noms', noms)
            rf = do_pm_request(thing)
            if noms[-1] == 'postUnitSystem':
                print('yoohoo xxxxxxxxxxxxx')
                print('yoohoo xxxxxxxxxxxxx')
                foo = copy.deepcopy(locals())
                return                            # tmp for debugging
                break                             # tmp for debugging
                                                  # but strangely, it does not
                                                  # work.
        else:    # it is an `item`.
            print(';;;;;;;;;;;;;;;;;;;;', noms)
            print(';;;;;;;;;;;;;;;;;;;;', 'doing an item... ')
            test_pm_section(pmjdoc, *noms)
  finally:
    globals().update(locals())


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


# Test individual services
# ######################################################################### #

smap = {
    'CRS Catalog': cat.service,
    'CRS Conversion': con.service,
    'Entitlements': entitlements.service,
    'Legal': legal.service,
    'Unit': unit.service,
}


def test_legal():
  try:
    pmjdoc = parsed_file_or_url(pm_files()[0])
    names = ['Core Services', 'Legal',]
    print(names[1])
    test_pm_section(pmjdoc, *names)
    print()
  finally:
    globals().update(locals())


def test_entitlements():
  try:
    pmjdoc = parsed_file_or_url(pm_files()[0])
    names = ['Core Services', 'Entitlements',]
    print(names[1])
    test_pm_section(pmjdoc, *names)
    print()
  finally:
    globals().update(locals())


def test_unit():
  try:
    """Unit service has a complex hierarchy of items & requests.
    """
    pmjdoc = parsed_file_or_url(pm_files()[0])
    names = ['Core Services', 'Unit', 'v3', 'catalog']
    names = ['Core Services', 'Unit', 'v3', 'conversion']
    names = ['Core Services', 'Unit', 'v3', 'measurement']
    names = ['Core Services', 'Unit', 'v3', 'unitsystem']
    names = ['Core Services', 'Unit', 'v3', 'unit', 'unitsystem']
    names = ['Core Services', 'Unit', 'v3', 'unit', 'measurement']
    names = ['Core Services', 'Unit', 'v3', 'unit', 'measurement', 'preferred']
    names = ['Core Services', 'Unit', 'v3', 'unit']    # has both
    names = ['Core Services', 'Unit']    # has both
    print(names[1])
    test_pm_section(pmjdoc, *names)
    print()
  finally:
    globals().update(locals())


def test_crs_catalog():
    pmjdoc = parsed_file_or_url(pm_files()[0])
    names = ['Core Services', 'CRS Catalog', 'V3']
    print(names[1])
    test_pm_section(pmjdoc, *names)
    print()


def test_crs_conversion():
    pmjdoc = parsed_file_or_url(pm_files()[0])
    print()
    names = ['Core Services', 'CRS Conversion', 'v3', 'convert']
    print(names[1])
    test_pm_section(pmjdoc, *names)
    names = ['Core Services', 'CRS Conversion', 'v3', 'convertTrajectory']
    test_pm_section(pmjdoc, *names)
    names = ['Core Services', 'CRS Conversion', 'v3', 'convertGeoJson']
    test_pm_section(pmjdoc, *names)
    names = ['Core Services', 'CRS Conversion', 'V3', 'v3', 'convertBinGrid']
    names = ['Core Services', 'CRS Conversion', 'v3', 'convertBinGrid']
#     test_pm_section(pmjdoc, *names)
# No such endpoint in 'v4'  swagger
    # TODO: note inconsistency with show_contents.
#     show_contents(pmjdoc, 'Core Services', 'CRS Conversion', 'v3', 'convertBinGrid')
# 
# but wait...
# Where did the 'V3' come from?
# It appeared at some point in my explorations.
# But seems to be superfluous.
# TODO: it must be related to the bug in show_contents


def test_all():
    test_crs_catalog()
    test_crs_conversion()
    test_legal()
    test_entitlements()
    test_unit()

