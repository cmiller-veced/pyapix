import os
from pyapix.apis.tools import parsed_file_or_url
from . import working_with_postman as wp
from .working_with_postman import (
    is_request, fetch_thing, 
    )


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


def test_fetch_thing():
  try:
    jdoc = parsed_file_or_url(pm_files()[0])
    rname = jdoc['item'][-4]['item'][-1]['item'][-1]['name']
    assert rname == '6c. Download file 3 from S3'
    # How to pull a particular thing of interest by name?
    n1 = jdoc['item'][-4]['name']
    n2 = jdoc['item'][-4]['item'][-1]['name']
    n3 = jdoc['item'][-4]['item'][-1]['item'][-1]['name']
    assert n3 == rname
    names = [
        'Dataset',
        'dataset-FileCollection.generic',
        '6c. Download file 3 from S3',
        ]
    n1, n2, n3 = names

    assert fetch_thing(jdoc) == jdoc
    r1 = fetch_thing(jdoc, 'Aggregate-WPC')            # request
    i1 = fetch_thing(jdoc, n1)                         # item
    i2 = fetch_thing(jdoc, n1, n2)                     # item
    r2 = fetch_thing(jdoc, n1, n2, n3)                 # request
    assert is_request(r1)
    assert is_request(r2)
    assert not is_request(i1)
    assert not is_request(i2)
    assert i1['name'] == n1
    assert i2['name'] == n2
    assert r2['name'] == n3
    tx = fetch_thing(jdoc, *names)
    assert tx == r2
    tx_auth = tx['request']['auth']        #['']
  finally:
    globals().update(locals())

