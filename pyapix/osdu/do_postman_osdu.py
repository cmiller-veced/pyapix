import os
from pyapix.tool.tools import parsed_file_or_url
from pyapix.tool import working_with_postman as wp
from pyapix.tool.working_with_postman import ( is_request, )
from pyapix.tool.exploratory import pop_key


version_format = """
pm.test('Version matches major.minor.patch format', function () {
  const responseJson = pm.response.json();
    pm.expect(responseJson.version).to.match(/\d*[.]\d*[.]\d*\S*/);
});
"""
status_200 = """
 pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
"""
status_ok = """
pm.test("Status description - OK.", function () {
    pm.response.to.have.status("OK");
});
"""
common_tests = [status_ok, status_200, version_format]
verbs = 'GET POST PATCH HEAD INFO DELETE PUT'

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


# TODO: OSDU events are largely low value, super-basic tests.
# Like the ones above.  Not worth pulling automatically.
def do_event(thing):
  try:
    event = thing['event']
    assert type(event) is list
    assert len(event) in [1, 2]
    empties = []
    for i, ev in enumerate(event):    # rm do-nothing events
        if ev['script']['exec'] == ['']:
            empties.append(i)
    empties.reverse()
    for i in empties:
        event.pop(i)
    if event == []:
        return
    assert len(event) == 1
    ev = event[0]
    assert type(ev) is dict
    assert sorted(list(ev)) == ['listen', 'script']
    assert ev['listen'] == 'test'
    es = ev['script']
    assert sorted(list(es)) == ['exec', 'type']
    assert es['type'] == 'text/javascript'
    ex = '\n'.join(es['exec'])    # the test code
    assert ex.strip()
    if ex in common_test or ex in status_200:
        ex = 'common'
  finally:
    globals().update(locals())



# TODO: this simply removes things for readability.
# Thus is exploratory.
@pop_key('event')
@pop_key('response')
def strip_it(req):
    req['url'] = req['request']['url']['raw']
    req.pop('request')
    return req


# TODO: this is hard-coded to crs{catalog,conversion} services.
def good_one(req):
    try:
        return req['request']['url']['path'][1] == 'crs'
    except KeyError:
        return False
 

def all_requests(pm_files):
    wp.check_do_item(pm_files)
    return wp.all_requests 
    # TODO: this is a bad way to return the value !!!!!!!!!!!!!
    # real bad !!!!!!


def filtered_list(lst, good_one):
    return [x for x in lst if good_one(x)]


# ########################################################################## # 

# TODO: this is NOT needed.  See crs_catalog client.
# but do not rush to delete.
def decode_query(reqs):
    svs = set()
    for req in reqs:
        name = req['name']
        if not 'url' in req:
            print(name, 'x'*44, 'no url')
            continue
        url = req['url'][26:]
        u, p = wp.decode_url(url)
        us = u.split('/')
        service = us[1] if len(us)>1 else 'unknown service'
        svs.add(service)
        if len(us)>1:
            endpoint = '/' + '/'.join(us[2:])
        else:
            endpoint = ''
        print(name)
        print(f'    {u}')
        print(f'    {service}.......{endpoint}')
        print(f'    {p}')
        print()
    print(svs)


ar = all_requests(pm_files)
crs_req = filtered_list(ar, good_one)
assert len(crs_req) == 14
crs_req = [strip_it(x) for x in crs_req]
assert len(crs_req) == 14
decode_query(crs_req)

ars = [strip_it(r) for r in all_requests(pm_files)]
#decode_query(ars)


# iterate over Postman file.                   DONE
# Find all calls to CRS Conversion.            DONE
# For each call, 
#     translate url(PM) to endpoint(pyapiX)    DONE
#     grab the parameters                      DONE
#     validate the parameters                  crs/conversion has none
#                                              I will have to make a client for
#                                              another service.
#                                              crs/catalog has some
# create client for crs/catalog                DONE
#     validate the parameters                  DONE
#
# store the parameters in yaml?


from pyapix.tool.working_with_postman import fetch_thing, insert_params

# TODO: mv to do_postman_osdu  DONE
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


# TODO: mv to do_postman_osdu?    YES  DONE
def is_bad_schema(schema):
    if schema == { 'required': [], 'properties': {},
     'additionalProperties': False, 'type': 'object'}:
        return True
    if schema['properties'] == {} and schema['additionalProperties'] == False:
        return True
    return False


# TODO: mv with func below  DONE
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
    return fix_colon_prefix(endpoint)

from working_with_postman import fix_colon_prefix

# TODO: (almost) nothing specific to CRS here.  DONE
# mv to somewhere
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
        try:
            v = service._validator(endpoint, verb)
        except BadEndpointOrVerb:
            bep = True
            assert endpoint.startswith('/legaltags/')
        if bep:
            valid_params = 'weird endpoint\n'
            valid_params += '>>>>>>>>>>>> ' + endpoint + '\n'
            valid_params += '>>>>>>>>>>>> ' + endpoint + '\n'
            valid_params += '>>>>>>>>>>>> ' + endpoint + '\n'
            valid_params += '>>>>>>>>>>>> ' + endpoint + '\n'
        else:
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

import json
from pyapix.tool.tools import parsed_file_or_url, list_of_dict_to_dict
one_dict = list_of_dict_to_dict()

service_parts = ['api', 'crs', 'catalog', 'conversion', 'search', 'storage',
                 'legal'
]



import json
from pyapix.tool.api_tools import Service
import crs_conversion_api as con
import crs_catalog_api as cat
import entitlements_api as entitlements
import legal_api as legal
import unit_api as unit

smap = {
    'CRS Catalog': Service(cat.call, cat._validator, cat.ends),
    'CRS Conversion': Service(con.call, con._validator, con.ends),
    'Entitlements': entitlements.service,
    'Legal': legal.service,
    'Unit': unit.service,
}


from pyapix.tool.api_tools import endpoints_ands_verbs
from pyapix.tool.tools import parsed_file_or_url, list_of_dict_to_dict
from pyapix.tool.working_with_postman import fetch_thing, insert_params
from pyapix.tool.do_postman_osdu import pm_files
from do_postman_osdu import is_version, is_bad_schema



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

from pyapix.tool.api_tools import BadEndpointOrVerb
# TODO: mv to ?  DONE and UNDONE
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
        thing = fetch_thing(pmjdoc, *noms)
        if is_request(thing):
            print(noms)
            rf = do_pm_request(thing)
        else:    # it is an `item`.
            print('# AHA!    brainwave!!! ')
            print('# AHA!    brainwave!!! ')
            print('We had expected a request but received an `item`.')
            print('We had expected a request but received an `item`.')
            print(noms)
            print('doing the item... ')
            test_pm_section(pmjdoc, *noms)
  finally:
    globals().update(locals())


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

    # TODO: this one has both `item`s and `request`s.
    # Work out how to deal with that.
    names = ['Core Services', 'Unit', 'v3', 'unit', 'getUnits']   # request

    names = ['Core Services', 'Unit', 'v3', 'unit', 'unitsystem']
    names = ['Core Services', 'Unit', 'v3', 'unit', 'measurement']
    names = ['Core Services', 'Unit', 'v3', 'unit', 'measurement', 'preferred']
    names = ['Core Services', 'Unit', 'v3', 'unit']    # has both
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
# TODO: it must be related to the bug way down below.



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
# TODO: change name to show_pm_contents
# or pm_show_contents
# or pm.show_contents
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

