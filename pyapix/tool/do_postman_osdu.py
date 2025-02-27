import os
from pyapix.tool.tools import parsed_file_or_url
from pyapix.tool import working_with_postman as wp
from pyapix.tool.working_with_postman import ( is_request, )


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


from pyapix.tool.exploratory import pop_key

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

