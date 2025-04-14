"""
The emphasis so far is on $refs in swagger docs.
That was a good starting point because it is a demanding problem.
Along the way I have
- gotten basic famiarity with jsonpath_ng
- inlined refs from first principles
  - thus paving the way for elimination of `jsonref` third party package.
- written recursive code over json data
- transformed json doc into a list of leaf-paths
- 

NEXT.  Read in a Postman file.
DONE.  And very nicely too.   Using leaf paths.

"""
import copy
from functools import singledispatch

from jsonpath_ng import parse, ext

from pyapix.tool.tools import parsed_file_or_url
from pyapix.osdu.client import unit


identity_func  = lambda x:x


def deep_key(obj, keys):
    """
    >>> [d0, _] = tdocs()
    >>> assert deep_key(d0, ['a', 'aa']) == 9
    >>> assert deep_key(d0, ['b', 'bb']) == 7
    >>> assert d0 == tdocs()[0]   # input not mutated
    """
    for key in keys:
        obj = obj[key]
    return obj


# Recursion over a heterogeneous data structure.
@singledispatch
def recur(arg, fun=identity_func):
    return fun(arg)

@recur.register
def _(arg: list, fun=identity_func):
    return [recur(fun(thing), fun) for thing in arg]

@recur.register
def _(arg: dict, fun=identity_func):
    return {key:recur(fun(arg[key]), fun) for key in arg}


def find_all_refs(jdoc):
    aps = leaf_paths(jdoc)
    return [lst for lst in aps if lst[-2] == '$ref']
            

# TODO: needs testing.
def replace_all_refs(jdoc):
    """
    Given: a json document with internal references.
    Return: the same document with the references in-lined.
    NO.  Update the document in place.
    """
    raw_ref_paths = find_all_refs(jdoc)
    [xinline_ref(x) for x in raw_ref_paths]
    # NOTE: not functional


def has_ref(dct):
    for key in dct:
        dkv = dct[key]
        if not type(dkv) is dict:
            continue
        if list(dkv) == ['$ref']:
            return key
    return None


# This belongs here.   It's been used to good effect on both PM and swagger.
# fails because of mutable keys?
from functools import lru_cache
#@lru_cache
def leaf_paths(jdoc):
    result = []

    @singledispatch
    def leaf_paths(arg, pth=[]):
        """
        Return a list of paths to each leaf in `jdoc`.
        """
        pth += [arg]
        result.append(pth)
        return pth

    @leaf_paths.register
    def _(arg: list, pth=[]):
        return [leaf_paths(thing, pth+[i]) for (i, thing) in enumerate(arg)]

    @leaf_paths.register
    def _(arg: dict, pth=[]):
        return [leaf_paths(arg[key], pth+[key]) for key in arg]
        return {key:leaf_paths(arg[key], pth+[key]) for key in arg}

    foo = leaf_paths(jdoc)
    # Undoing the nesting of `foo` is non-trivial.
    # Thus I like the current solution.
    return result


def path_prep(thing):
    if type(thing) is int:
        return f'[{thing}]'
    try:
        int(thing)
        return f'"{thing}"'
    except ValueError:
        pass
    ptriggers = ['/', ' ', '$']
    if any(t in thing for t in ptriggers):
        return f'"{thing}"'
        # TODO: this will be a problem if the user tries using ".   ?
        # TODO: ^^^^^ meanging "double quotes"... ^^^^^^^^^^ 
    return thing


# belongs here
def to_jsonpath(lst):
    return '.'.join(path_prep(x) for x in lst)


def reference_value(jdoc, raw_ref):
    ref_path = raw_ref.split('/')[1:]
    return deep_key(jdoc, ref_path)


# # TODO: eliminate this one.
# def inline_ref(dct, ref_key, jdoc):
#     dct[ref_key] = deep_key(jdoc, dct[ref_key]['$ref'].split('/')[1:])
#     return 'ok'


# TODO: rename
def xinline_ref(rp, jdoc):
    """
    Update jdoc.
    Not functional but copying is expensive.
    >>> rp = ['definitions', 'VersionInfo', 'properties', 'connectedOuterServices', 'items', '$ref', '#/definitions/ConnectedOuterService']
    """
    raw_ref = rp[-1]
    rv = reference_value(jdoc, raw_ref)
    path_to_thing = to_jsonpath(rp[:-2])
    je = ext.parse(path_to_thing)
    [dm] = je.find(jdoc)
    dm.full_path.update(jdoc, rv)
#    print(path_to_thing, raw_ref)



# test code below
# ########################################################################## #
# ########################################################################## #
# ########################################################################## #


def tdocs():
    jd1 = dict(
        a=dict(
            aa=9,
            bb=[
                dict(aaa=1),
                dict(aaa=2),
            ],
        ),
        b=dict(
            aa=8,
            bb=7,
            cc='x',
        ),
    )
    jd2 = dict(
        a=dict(
            bb=[
                dict(aaa=3),
            ],
        ),
        b=dict(
            bb=3,
        ),
    )
    return (jd1, jd2)


book_data = {
  "store": {
    "book": [
      {
        "category": "reference",
        "author": "Nigel Rees",
        "title": "Sayings of the Century",
        "price": 8.95
      },
      {
        "category": "fiction",
        "author": "Herman Melville",
        "title": "Moby Dick",
        "isbn": "0-553-21311-3",
        "price": 8.99
      },
      {
        "category": "fiction",
        "author": "J.R.R. Tolkien",
        "title": "The Lord of the Rings",
        "isbn": "0-395-19395-8",
        "price": 22.99
      }
    ],
    "bicycle": {
      "color": "red",
      "price": 19.95
    }
  },
  "expensive": 10
}


def delete_all_refs(jdoc):
    """Maybe not useful but demonstrates how to operate.
    NOTE:  non-functional.
    """
    aps = leaf_paths(jdoc)
    refs = [p[:-2] for p in aps if p[-2] == '$ref']
    jp2 = [to_jsonpath(p) for p in refs]
    je2 = [ext.parse(p) for p in jp2]    
    ms = [je.find(jdoc)[0] for je in je2]    # 
    dels = [m.full_path.update(jdoc, {}) for m in ms]



def test_path_extraction():
  try:
    (jd1, jd2) = tdocs()
    lp2 = leaf_paths(jd2)
    assert lp2 == [['a', 'bb', 0, 'aaa', 3], ['b', 'bb', 3]]
    vs2 = [p[-1] for p in lp2]
    lp2 = [p[:-1] for p in lp2]
    assert lp2 == [['a', 'bb', 0, 'aaa'], ['b', 'bb']]
    jp2 = [to_jsonpath(p) for p in lp2]
    je2 = [ext.parse(p) for p in jp2]    
    jm2 = [je.find(jd2)[0].value for je in je2]    # kicks ass !!!!!!!
    assert jm2 == vs2

    lp1 = leaf_paths(jd1)
    assert lp1 == [['a', 'aa', 9], ['a', 'bb', 0, 'aaa', 1], ['a', 'bb', 1, 'aaa', 2], ['b', 'aa', 8], ['b', 'bb', 7], ['b', 'cc', 'x']]
    vs1 = [p[-1] for p in lp1]
    lp1 = [p[:-1] for p in lp1]
    assert lp1 == [['a', 'aa'], ['a', 'bb', 0, 'aaa'], ['a', 'bb', 1, 'aaa'], ['b', 'aa'], ['b', 'bb'], ['b', 'cc']]
    jp1 = [to_jsonpath(p) for p in lp1]
    je1 = [ext.parse(p) for p in jp1]    
    jm1 = [je.find(jd1)[0].value for je in je1]    # kicks ass !!!!!!!
    assert jm1 == vs1

    jdoc = parsed_file_or_url(unit.config.swagger_path)
    lpju = leaf_paths(jdoc)

#    assert len(lpju) == 6610   # with inline $refs
    assert len(lpju) == 1125   # with $refs

    vsu = [p[-1] for p in lpju]
    lpu = [p[:-1] for p in lpju]
    jpu = [to_jsonpath(p) for p in lpu]
    for (i, p) in enumerate(jpu):
        je = ext.parse(p)
        ju = je.find(jdoc)
        v = ju[0].value
        print(p, v)
        assert v == vsu[i]

  finally:
    globals().update(locals())


def test_refs():
  try:
    jdoc = parsed_file_or_url(unit.config.swagger_path)
    c = copy.deepcopy(jdoc)

    assert recur(jdoc) == jdoc                       # OK
    assert recur(jdoc, identity_func) == jdoc        # OK

    raw_ref_paths = find_all_refs(jdoc)
    assert len(raw_ref_paths) == 85

    # in-line individual refs
    for rp in raw_ref_paths:
        xinline_ref(rp, c)    # update `c` in place.
        old_thing = deep_key(jdoc, rp[:-2])
        new_thing = deep_key(c, rp[:-2])

        assert len(old_thing) == 1
        assert old_thing['$ref'].startswith('#/definitions/')

        assert type(new_thing) is dict
        assert len(new_thing) > 1
        assert '$ref' not in new_thing
    # All refs are now in-lined. 
    assert not '$ref' in str(c)
    assert '$ref' in str(jdoc)
    
    ps = c['paths']['/v3/unitsystem/list']['get']['responses']['200']['schema']
    assert ps == {'type': 'object', 'properties': {'count': {'type': 'integer', 'format': 'int32'}, 'offset': {'type': 'integer', 'format': 'int32'}, 'totalCount': {'type': 'integer', 'format': 'int32'}, 'unitSystemInfoList': {'type': 'array', 'items': {'type': 'object', 'properties': {'ancestry': {'type': 'string'}, 'description': {'type': 'string'}, 'name': {'type': 'string'}, 'persistableReference': {'type': 'string'}}}}}}
    # real good test because the ref contains a ref.


    # A good test of refs with a small document
    jdoc = {'foo': {'$ref': '#/definitions/bar'}, 'definitions': {'bar': 'bat'}} 
    [raw_ref_path] = find_all_refs(jdoc)
    xinline_ref(raw_ref_path, jdoc)    # update `jdoc` in place.
    assert jdoc == {'foo': 'bat', 'definitions': {'bar': 'bat'}} 


    # Delete all $ref fwiw.
    jdoc = parsed_file_or_url(unit.config.swagger_path)
    delete_all_refs(jdoc)
    assert '$ref' not in str(jdoc)

  finally:
    globals().update(locals())


# def test_all():
#     test_refs()
#     test_path_extraction()
#     test_namespace()


# ###########################
# ###########################
# ###########################


# TODO: put this with exploratory code.
def namespacify(thing):
    ugly_hack = json.dumps(thing, indent=1)
#    ugly_hack = json.dumps(thing)   # when ugly_hack is no longer needed we
#    will use this line instead.
    return json.loads(ugly_hack, object_hook=lambda d: SimpleNamespace(**d))
    # ugly_hack:    indent=1
    # ugly_hack is required, and works because ...
    # By the way, this specific problem (with json.dumps) can be bypassed by passing any of the "special" parameters dumps accepts (e.g indent, ensure_ascii, ...) because they prevent dumps from using the JSON encoder implemented in C (which doesn't support dict subclasses such as rpyc.core.netref.builtins.dict). Instead it falls back to the JSONEncoder class in Python, which handles dict subclasses.
    # https://github.com/tomerfiliba-org/rpyc/issues/393


import jsonref
import json
from types import SimpleNamespace
def test_namespace():    # dict => namespace
  try:
#    rs = raw_swagger(pet_swagger_local)
    rs = parsed_file_or_url(unit.config.swagger_path)
    ns0 = namespacify(rs)

    with_refs = jsonref.loads(json.dumps(rs))
#     ns = namespacify(with_refs)     # ugly_hack required for this 
# 
#     assert ns0.definitions.Pet.properties.category == namespacify(rs['definitions']['Pet']['properties']['category'])
# 
#     assert ns.definitions.Pet.properties.category == namespacify(with_refs['definitions']['Pet']['properties']['category'])
#     assert ns.definitions.Pet.properties.category == namespacify(deep_key('definitions Pet properties category', with_refs))
# 
#     # convert namespace back to dict.
#     v0 = vars(ns)  # ok but not recursive
# 
#     # recursively convert namespace back to dict.
#     v = json.loads(json.dumps(ns, default=lambda s: vars(s)))

  finally:
    globals().update(locals())


# # swagger paths.  As contrasted with leaf paths.
# def all_paths(jdoc):
#     return list(jdoc['paths'])

# xinline_ref(rp, jdoc)
# rp = ['definitions', 'VersionInfo', 'properties', 'connectedOuterServices', 'items', '$ref', '#/definitions/ConnectedOuterService']
  
def test_one_ref():
    jdoc = parsed_file_or_url(unit.config.swagger_path)
    ep = '/v3/unitsystem/list'
    epi = jdoc['paths'][ep]['get']['responses']
    ep2 = jdoc['paths'][ep]['get']['responses']['200']
    o = copy.deepcopy(ep2)
    s0 = copy.deepcopy(jdoc['paths'][ep]['get']['responses']['200'])    #['schema']

    hr = has_ref(ep2)
#     xinline_ref(ep2, hr, jdoc)
#     ep3 = ep2['schema']['properties']['unitSystemInfoList']
#     hr = has_ref(ep3)
#     xinline_ref(ep3, hr, jdoc)
# 
#     s1 = jdoc['paths'][ep]['get']['responses']['200']    #['schema']
# 
# #     x = inline_section(ep2, jdoc)

    epn = namespacify(epi)
    epn = namespacify(ep2)
    globals().update(locals())

