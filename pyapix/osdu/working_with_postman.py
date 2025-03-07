"""
Working with Postman files.
The focus is on OSDU preshipping.
"""

import os
import json
from functools import lru_cache
import typing
from typing import TypedDict
from typing import Required, NotRequired

from pyapix.tool.tools import parsed_file_or_url
from pyapix.tool.exploratory import pop_inputs, pop_key

items_seen = []
requests_seen = []
all_requests = []


# TODO: rename?   This is used in other two other files.
def check_do_item(pm_files):
  try:
    global all_requests
    all_requests = []
    for fpath in pm_files():
        with open(fpath) as fh: 
            jdoc = json.load(fh)
        print(fpath.split('/')[-1].split('.')[0])
        do_item(jdoc)
        print()
  finally:
    globals().update(locals())


# TODO: review
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


# untidy
def do_request(thing, indent):
  try:
    assert is_request(thing)
    global all_requests
    all_requests.append(thing)
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


# solid
# TODO: maybe call it fetch_postman_thing
def fetch_thing(jdoc, *names):
    """
    >>> innermost = [
    ...     dict(name='bat', t=1),
    ...     dict(name='x', t=2),
    ...     dict(name='y'),
    ... ]
    ... 
    >>> mid = [
    ...     dict(name='bar', item=innermost),
    ...     dict(name='c', t=3, item=[]),
    ...     dict(name='d'),
    ... ]
    ... 
    >>> outermost = dict(item=[
    ...     dict(name='foo', item=mid),
    ...     dict(name='a', item=[]),
    ...     dict(name='b'),
    ... ])
    ... 

    >>> assert fetch_thing(outermost) == outermost
    >>> assert fetch_thing(outermost, 'foo') == dict(name='foo', item=mid)
    >>> assert fetch_thing(outermost, 'foo', 'bar') == dict(name='bar', item=innermost)
    >>> assert fetch_thing(outermost, 'foo', 'bar', 'bat') == {'name': 'bat', 't': 1}
    """
    sub = jdoc
    for name in names:
        for thing in sub['item']:
            if thing['name'] == name:
                sub = thing
                break     # the first thing with that name
    return sub


# solid
# OK.  Successfully decoded all bodies in OSDU.
def decode_body(body):
    bm = body['mode']
    assert bm in ['raw', 'urlencoded', 'file']
    br = body[bm]
    if (type(br) is not str) or (not br):
        return br
    return json.loads(br)


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

# used once.
def write_data():
    # TODO: write petstore to yaml.
    # !!!!!!!!!! WARNING !!!!!!!!!!
    # Use great caution when writing yaml because it can come out quite garbled.
    # All info will be there but with references not very readable.
#    from pyapix.test_data import petstore
    import yaml
    fname = 'petstore_dataX.yaml'
    data = petstore.__dict__
    for key in dubs:
        data.pop(key)
    with open (fname, 'w') as fh:
        yaml.dump(data, fh)

# not used
@lru_cache
def postman_schema():
    # all postman schemas == v1.0.0  v2.0.0  v2.1.0
    # OSDU Preshipping postman files have this...
    'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'
    # for schema.  But that link is   301 Permanently moved.
    postman_schema = 'https://schema.postman.com/collection/json/v2.1.0/draft-07/collection.json'
    return parsed_file_or_url(postman_schema)


# TODO: is this needed?
def decode_url(url):
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


#    Newly moved to this file.......


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
  try:
    eps = [e for (e,v) in service.ends]   # all endpoints for swagger
    up = url['path']
    endpoint = url['raw'].replace(url['host'][0], '')
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
  finally:
    globals().update(locals())


