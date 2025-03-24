"""
Working with Postman files.
The focus is on OSDU preshipping.
"""

import os
import json
from functools import lru_cache
from collections import defaultdict

from pyapix.tool.tools import parsed_file_or_url
from pyapix.tool.jtool import leaf_paths, to_jsonpath
from jsonpath_ng import ext
from pyapix.tool.exploratory import pop_inputs, pop_key


# TODO: if any of the url/path/query parsing stuff is needed, it is this.
def fix_colon_prefix(path):
  try:
    """
    Accomodate a Postman quirk.   Or is it an OSDU quirk?
    >>> path = '/foo/:bar/bat/:ratHatCat'
    >>> assert fix_colon_prefix(path) == '/foo/{{bar}}/bat/{{rat_hat_cat}}'
    """
    if ':' not in path:
        return path
    words = path.split('/')
    for (i, word) in enumerate(words):
        if word.startswith(':'):
            new = []
            for char in word[1:]:
                if char.isupper():
                    new.append('_')
                    new.append(char.lower())
                else:
                    new.append(char)
#            words[i] = '{{' + ''.join(new) + '}}'
            words[i] = '{' + ''.join(new) + '}'
    return '/'.join(words)
  finally:
    globals().update(locals())


# solid below here.
# ######################################################################## #


# solid
def insert_params(template, parameters):
    """
    >>> url = '{{base_url}}/api/search/v2/query'
    >>> ps = dict(base_url='xxxxxxxx')
    >>> x = insert_params(url, ps)
    >>> assert x == 'xxxxxxxx/api/search/v2/query'

    >>> template = 'xyz {{abc}} wvp'
    >>> abc = 'xxxxxxxx'
    >>> x = insert_params(template, locals())
    >>> assert x == 'xyz xxxxxxxx wvp'
    """
    from jinja2 import select_autoescape 
    from jinja2 import Environment as j2Environment
    env = j2Environment(autoescape=select_autoescape())
    return env.from_string(template).render(**parameters)


# solid
# OK.  Successfully decoded all bodies in OSDU.
def decode_body(body):
    bm = body['mode']
    globals().update(locals())
    assert bm in ['raw', 'urlencoded', 'file', 'formdata']
    br = body[bm]
    if (type(br) is not str) or (not br):
        return br
    return json.loads(br)


# TODO: is this needed?  Yes, it gets called, anyway.
def decode_url(url):
    """For working with Postman.
    But should be much more general.
    Pull query parameters, if present.
    """
    if not '?' in url:
        return (fix_colon_prefix(url), '')
    assert url.count('?') == 1
    front, end = url.split('?')
    parts = end.split('&')
    assert  all(len(x.split('='))==2 for x in parts)
    query_params = dict(x.split('=') for x in parts)
    front = fix_colon_prefix(front)
    return (front, query_params)


# solid
class Environment:
    """A hierarchy of environments, ala Postman.
    >>> environment = Environment()
    >>> assert 'k' not in environment.general
    >>> assert 'k' not in environment.current
    >>> environment.request['k'] = 'v'
    >>> assert environment.current['k'] == 'v'
    >>> assert 'k' not in environment.general
    >>> environment.reset()
    >>> assert environment.current == {}
    >>> assert environment.request == {}
    """
    def __init__(self):
        self._current = {}
        self.general = {}
        self.collection = {}
        self.sequence = {}
        self.request = {}

    def update(self):
        for source in [self.general, self.collection, self.sequence, self.request]:
            self._current.update(source)
#        globals().update(self._current)    # ?

    @property
    def current(self):
        self.update()
        return self._current

    def reset(self):
        self.general = {}
        self.collection = {}
        self.sequence = {}
        self.request = {}
        self._current = {}


# postman general
def pm_item_dict(jdoc):
    item_dict = defaultdict(lambda:[])
    unique_requests = set()
    pleaf = leaf_paths(jdoc)

    for path in pleaf:
        if 'request' in path:
            idx = path.index('request')
            unique_requests.add(to_jsonpath(path[:idx]))

    for request_path in sorted(unique_requests, key=sort_thing):
        je = ext.parse(request_path)
        [rm] = je.find(jdoc)
        rfp = str(rm.full_path)
        trunc = rfp[:rfp.rindex('.')]
        item_dict[trunc].append(rfp)

#    assert len(unique_requests) == 152
    return item_dict


# postman general
def sort_thing(jpath):
    """
    # TODO: this would be a good homework assignment.
    # With follow-up forbidding use of `eval`.
    jpath = 'item.[1].item.[5].item.[0].item.[1].item.[1].item'
    """
    inner = jpath.replace('item', '').replace('.', '').replace(']', ', ').replace('[', '')
    return eval('(' + inner + ')')


# untidy
# OK.  Successfully decoded all headers in OSDU.
def do_headers(headers):
  try:
    return {h['key']: h['value'] for h in headers}

    standard_header_keys = ['key', 'type', 'value']
    standard_header_keys = ['key', 'value']

    assert type(headers) is list
    if not headers:
        return headers
    assert len(headers) < 14
    for header in headers:
        assert all(k in header for k in standard_header_keys)
#        hkeys = sorted(list(header.keys()))
    return [sorted(list(h.keys())) for h in headers]
    return headers
  finally:
    globals().update(locals())


# TODO: review
def do_item(thing, indent=0):
  try:
    if not 'item' in thing:
        return do_request(thing, indent)
    name = thing['name'] if 'name' in thing else 'base'
    assert not is_request(thing)
    items = thing['item']
    assert type(items) is list
    print('i', ' '*indent, name, len(items))
    for ithing in items:
        assert type(ithing) is dict
        if 'item' in ithing:
            do_item(ithing, indent+4)
        else:   # it is a request
            print(' '*(indent+4), ithing['name'])
            do_request(ithing, indent+4)
  finally:
    globals().update(locals())


report_mode = False
report_mode = True
debug_mode = report_mode and False


def fetch_args(url_raw, request):
  try:
    if 'body' in request:
        bm = request['body']['mode']
        bd = decode_body(request['body'])
    else:
        bm = 'NO body'
        bd = None

    params = {}
    (url, qparams) = decode_url(url_raw)
    if qparams: params['query'] = qparams

    if (bd and bd != {''}):
        params['body'] = bd 
 
    return (url, params)
  finally:
    globals().update(locals())


def find_service(url, verb):
  try:
    for sname in epdict:
        for (ep, v) in epdict[sname]:
            if url.endswith(ep) and v==verb:
                return (sname.lower(), ep)
    # osdu-specific
    parts = url.split('/api/')    # OSDU specific
    last = parts[-1]
    t = last.split('/')[0]
    s = t.replace('{', '').split('_')[0].lower()
    return (s, '?')
  finally:
    globals().update(locals())


def test_find_service():
  try:
    uv = ('/api/storage/v2/records/{{wipRecordId}}', 'delete')
    uv = ('/api/storage/v2/records/{{recordIdsSC}}', 'delete')
    uv = ('/api/storage/v2/records/{{recordIds}}', 'delete')
    fs = find_service(*uv)
    # TODO: fix
    # May have to look at verb and guess about endpoint.
    # Although, in this case, guessing is not required.  Just more complex logic
    # for the case of {{theseThings}}.
    # Not too bad really.
    """
    >>> storage.ends [
    ('/records', 'put'), 
    ('/records', 'patch'), 
    ('/records/copy', 'put'),
    ('/records/{id}:delete', 'post'), 
    ('/records/delete', 'post'),
    ('/records/{id}', 'get'),
    ('/records/{id}', 'delete'), 
    ('/records/{id}/{version}', 'get'),
    ('/records/versions/{id}', 'get'), 
    ('/records/{id}/versions', 'delete'), 

    ('/query/records', 'get'), 
    ('/query/records', 'post'),
    ('/query/records:batch', 'post'), 

    ('/liveness_check', 'get'), 
    ('/info', 'get'),

    ('/replay/status/{id}', 'get'),
    ('/replay/status/{id}', 'security'), 
    ('/replay', 'post'), 

    ('/whoami', 'get'),
    ('/whoami', 'put'), 
    ('/whoami', 'post'), 
    ('/whoami', 'delete'), 
    ('/whoami', 'options'),
    ('/whoami', 'head'), 
    ('/whoami', 'patch')]
    """

  finally:
    globals().update(locals())


from pyapix.osdu.client.bunch import (search, notification, register, 
    storage,
    schema,
    dataset,
    schema_upgrade,
    secret_v1,
    secret,
    unit, legal, entitlements, crs_catalog, crs_conversion,
)

clients = (unit, legal, entitlements, crs_catalog, crs_conversion, 
    search, notification, register, schema, schema_upgrade, secret_v1, secret,
    dataset,
    storage,
   )
# below depends on `clients`.
epdict = {s.name: set((ep, v) for (ep, v) in s.ends) for s in clients}
odict = {s.name.lower():s for s in clients}
cdict = defaultdict(lambda:'?')
cdict.update(odict)


def do_request(thing, indent):
  try:
    # TODO: validation:  
    #     identify service, endpoint, verb   OK
    #     fetch data from `thing`            OK
    #     create/fetch api client            OK
    #     fetch validator                    OK
    #     validate data                      OK
    #  OK for some service/endpoint/verb combinations.
    #  Many gaps.

    request = thing['request']
    url_raw = request['url']['raw']
#    (url, _) = decode_url(url_raw)
    (url, params) = fetch_args(url_raw, request)

    verb = request['method'].lower()
    (sname, ep) = find_service(url, verb)      # (service_name, endpoint)
    service = cdict[sname]
    if (type(service) is not str) and (ep != '?'):
        vd = service.validator(ep, verb)
#        if not vd.is_valid(params): vd.validate(params)
        vp = 'OK' if vd.is_valid(params) else 'NO'
    else:
        vp = 'unknown'

    dh = do_headers(request['header'])

    if 'auth' in request:
        ra = request['auth']

    if report_mode:
#        if qparams: assert type(qparams) is dict
        assert type(request) is dict
        for word in ['method', 'header', 'url']:
            assert word in request
        other_words = ['auth', 'body', 'description']  # may be in request
        print(' '*(indent+2), 'url_raw', url_raw)
        print(' '*(indent+2), sname, ep, verb)
        print(' '*(indent+2), params)
        print(' '*(indent+2), 'valid params?', vp)

    if debug_mode:
        print(' '*(indent+2), dh)
        print(' '*(indent+2), len(dh))
        print(' '*(indent+2), bm)
        print(' '*(indent+2), bd)

  finally:
    globals().update(locals())

#from pyapix.osdu.client import search


# Test
# ########################################################################## #
# ########################################################################## #
# ########################################################################## #


def test_pmx():
  try:
    from pyapix.osdu.config import path
    for fpath in [
            path.policy,
            path.wellbore_ddms,
            path.core_services,
      ]:
        jdoc = parsed_file_or_url(fpath)
        item_dict = pm_item_dict(jdoc)
    #    assert len(item_dict) == 42
        print('========================================================')

        # NOTE This is snappy.  Transforms PM doc into a dict where the keys are
        # terminal `item`s and the values are the list of `request`s that fall under
        # that `item`.
        # Now it is easy to iterate.
        for ipath in item_dict:
            print(ipath)
            for rpath in item_dict[ipath]:
                je = ext.parse(rpath)
                [rm] = je.find(jdoc)
                rfp = str(rm.full_path)
                rmv = rm.value
                print('  ', rpath, rmv['name'])
                dr = do_request(rmv, 4)

  finally:
    globals().update(locals())


def test_environment():
    environment = Environment()
    assert environment.current == {}
    things = [
        (environment.general, None),
        (environment.collection, 2),
        (environment.sequence, 22),
        (environment.request, 222),
    ]
    for (thing, value) in things:
        thing['foo'] = value
    assert 'foo' in environment.current
    assert environment.current['foo'] == environment.request['foo']
    for (thing, value) in things:
        assert thing['foo'] == value
    environment.reset()
    assert environment.current == {}


def read_it():
    return environment.current['a']

def write_it():
    environment.request['a'] = 4

def setup_environment():
    environment = Environment()
    environment.collection['a'] = 1
    environment.request['a'] = 2
    globals().update(locals())

def test_environment2():
    """Demonstrate how to read/write a global environment.
    """
    setup_environment()
    assert read_it() == 2
    environment.request.pop('a')
    assert read_it() == 1
    environment.request['a'] = 3
    assert read_it() == 3
    write_it()
    assert read_it() == 4


def test_decode_url():
  try:
    urls = """
/crs/catalog/v3/coordinate-reference-system?dataId=Geographic2D:EPSG::4158&recordId=osdu:reference-data--CoordinateReferenceSystem:Geographic2D:EPSG::4158
/register/v1/action/:id
/register/v1/action:retrieve
/register/v1/subscription/:id/secret
/unit/v3/unit/unitsystem?unitSystemName=English&ancestry=Length&offset=0&limit=100
/unit/v3/unit/measurement?ancestry=1
/unit/v3/conversion/abcd?namespaces=Energistics_UoM&fromSymbol=ppk&toSymbol=ppm
/unit/v3/conversion/abcd
/legal/v1/legaltags:query?valid=true
/entitlements/v2/groups/:groupEmail/members/:memberEmail
/entitlements/v2/members/:memberEmail/groups?type=DATA
    """.split()
    for url in urls:
        front, query_params = decode_url(url)
        print(url)
        print(front)
        print(query_params)
        print()

    # One-time dev stuff below.....
    eswagger = '~/osdu/service/entitlements/docs/api/entitlements_openapi.yaml'
    ejson = parsed_file_or_url(eswagger)
    eps = list(ejson['paths'])
    # AHA!    brainwave!!! 
    # The OSDU openapi files violate the standard thus...
    # /groups/:groupEmail/members/:memberEmail
    # should be
    # /groups/{group_email}/members/{member_email}
    # I guess they think they know better.

    lswagger = '~/osdu/service/legal/docs/api/legal_openapi.yaml'
    ljson = parsed_file_or_url(lswagger)
    lps = list(ljson['paths'])

    sp = '~/osdu/service/register/docs/api/register_openapi.yaml'
    js = parsed_file_or_url(sp)
    rps = list(js['paths'])

  finally:
    globals().update(locals())


def test_all():
    test_pmx()
    test_environment()
    test_environment2()
    test_decode_url()


# OK
# Now we can
# 1. Recursively iterate over all things.
# 2. Fetch arbitrary, deeply nested things.
# TODO: 
# - run individual request.
# - run a sequence of requests.
# - cleanup the jdoc by removing empty things.
# - add and subtract things.


# Questionable usefulness below
# ########################################################################## #


