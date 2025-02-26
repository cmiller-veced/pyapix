"""
Working with Postman files.

The focus is on OSDU preshipping.
I've made good progress deciphering body and headers for each request.
But to make further progress I need to be able to hit the endpoints.
NO.
One more place where I could make progress now is in replacing vars.
and validation.

"""
import os
import json
from functools import lru_cache
from pyapix.apis.tools import parsed_file_or_url, raw_file_or_url
import typing
from typing import TypedDict
from typing import Required, NotRequired

from .exploratory import pop_inputs, pop_key

items_seen = []
requests_seen = []


def check_do_item(pm_files):
  try:
    for fpath in pm_files():
        with open(fpath) as fh: 
            jdoc = json.load(fh)
        print(fpath.split('/')[-1].split('.')[0])
        do_item(jdoc)
        print()
  finally:
    globals().update(locals())


def do_item(thing, indent=0):
  try:
    is_item_or_request_but_not_both(thing)
    if not 'item' in thing:
        return do_request(thing, indent)
    name = thing['name'] if 'name' in thing else 'base'
    global items_seen
    items_seen.append(name)
    assert not is_request(thing)
    assert has_items(thing)
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


# OK.  Successfully decoded all bodies in OSDU.
def decode_body(body):
  try:
    bm = body['mode']
    assert bm in ['raw', 'urlencoded', 'file']
    br = body[bm]
    if (type(br) is not str) or (not br):
        return br
    return json.loads(br)
  finally:
    globals().update(locals())


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


def do_request(thing, indent):
  try:
    assert is_request(thing)
    assert not has_items(thing)
    global requests_seen
    requests_seen.append(thing['name'])
    request = thing['request']
    assert type(request) is dict
    for word in ['method', 'header', 'url']:
        assert word in list(request)
    other_words = ['auth', 'body', 'description']  # may be in list(request)

    url_raw = request['url']['raw']
    print(' '*(indent+2), url_raw)

    dh = do_headers(request['header'])
#    print(' '*(indent+2), dh)
#    print(' '*(indent+2), len(dh))

    if 'body' in request:
        bm = request['body']['mode']
        bd = decode_body(request['body'])
    else:
        bm = bd = 'NO body'
#    print(' '*(indent+2), bm)
#    print(' '*(indent+2), bd)
    if 'auth' in request:
        ra = request['auth']
  finally:
    globals().update(locals())


def exp_with_postman_schema():
    pm_schema = parsed_file_or_url('~/local/postman/2.1.0.json')
    request_schema = pm_schema['definitions']['request']
    pm_defs = pm_schema['definitions']
    ['$schema', '$id', 'title', 'description', 'oneOf']
    ['url', 'auth', 'proxy', 'certificate', 'method', 'description', 'header', 'body']

    script_schema = pm_schema['definitions']['script']
    ['$schema', '$id', 'title', 'type', 'description', 'properties']
    ['id', 'type', 'exec', 'src', 'name']


def exp_with_TypedDict():
    Point2D = TypedDict('Point2D', {'in': int, 'x-y': int})
    # TODO: NOTE
    # This is interesting.  Keys that are keywords or contain '-'.
    # Could be useful when we want to use keys like 
    # /zones/:type/:zoneId
    Point2D = TypedDict('Point2D', {'/zones/:type/:zoneId': int, 'x-y': int})

    p2 = Point2D( {'z': 3, 'label': 'bad'})
    p2 = Point2D(t= 3, label= 'bad')


class Request(TypedDict, total=True):
    header: Required[dict]
    body: typing.Dict  = None
    description: str  = None
    method: str     # enum
    url: str     # matching a regex

class MyParameters(TypedDict, total=True):
    header: NotRequired[dict]
    body: NotRequired[dict]
    query: NotRequired[dict]
    args: NotRequired[dict] = {}
 
class MyRequest(TypedDict, total=True):
    endpoint: str     # matching a regex
    method: str     # enum
    parameters: MyParameters = None
    post_test:  typing.Callable   = lambda _:None
    # TODO?: auth: dict  # or such?

# MyRequest and MyParameters can be used together to create a Request object.
# That will be the mapping between my stuff and Postman schema.

mr = MyRequest()
mr = MyRequest(ep=1)
mr = MyRequest(endpoint=1, method='have', parameters={})

rt = Request()
rt = Request(x=2)
rt = Request(header=2, url='u', method='m')


# TODO: maybe call it fetch_postman_thing
@pop_key('response')
@pop_key('event')
def fetch_thing(jdoc, *names):
  try:
    """ snappy
    But definitely needs a doctest.
    Also is near to being quite general.
    The two hard-coded names keep it from being general.
    """
    sub = jdoc
    for name in names:
        for thing in sub['item']:
            if thing['name'] == name:
                sub = thing
                break     # the first thing with that name
    return sub
  finally:
    globals().update(locals())

# OK
# Now we can
# 1. Recursively iterate over all things.
# 2. Fetch arbitrary, deeply nested things.
# TODO: 
# - run individual request.
# - run a sequence of requests.
# - cleanup the jdoc by removing empty things.
# - add and subtract things.


def has_items(thing):
    return 'item' in thing

def is_request(thing):
    return 'request' in thing

verified_mutually_exclusive = []
def is_item_or_request_but_not_both(thing):
    assert is_request(thing) or has_items(thing)
    assert not (is_request(thing) and has_items(thing))
    global verified_mutually_exclusive
    
    name = thing['name'] if 'name' in thing else 'base'
    verified_mutually_exclusive.append(name)
    # TODO: this is a job for a closure.
    # TODO: appears to be capturing `items` but not `requests`.
    # pprint(set(verified_mutually_exclusive))


def write_data():
    # TODO: write petstore to yaml.
    # !!!!!!!!!! WARNING !!!!!!!!!!
    # Use great caution when writing yaml because it can come out quite garbled.
    # All info will be there but with references not very readable.
#    from pyapix.test_data import petstore
    import yaml
    globals().update(locals())
    fname = 'petstore_dataX.yaml'
    data = petstore.__dict__
    for key in dubs:
        data.pop(key)
    with open (fname, 'w') as fh:
        yaml.dump(data, fh)


@lru_cache
def postman_schema():
    # all postman schemas == v1.0.0  v2.0.0  v2.1.0
    # OSDU Preshipping postman files have this...
    'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'
    # for schema.  But that link is   301 Permanently moved.
    postman_schema = 'https://schema.postman.com/collection/json/v2.1.0/draft-07/collection.json'
    return parsed_file_or_url(postman_schema)


def fix_colon_prefix(path):
  try:
    """
    Accomodate a Postman quirk.
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
            words[i] = '{{' + ''.join(new) + '}}'
    return '/'.join(words)
  finally:
    globals().update(locals())


def decode_url(url):
  try:
    """For working with Postman.
    But should be much more general.
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
  finally:
    globals().update(locals())


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
    #def templatified(s): return s.replace('{', '{{').replace('}', '}}')
    from jinja2 import select_autoescape 
    from jinja2 import Environment as j2Environment
    env = j2Environment(autoescape=select_autoescape())
    return env.from_string(template).render(**parameters)


class Environment:
    """A hierarchy of environments, ala Postman.
    >>> environment = Environment()
    >>> assert 'k' not in environment.general
    >>> assert 'k' not in environment.current
    >>> environment.request['k'] = 'v'
    >>> assert 'k' not in environment.general
    >>> assert environment.current['k'] == 'v'
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


def test_environment_update():
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

