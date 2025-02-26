from functools import wraps
from inspect import signature


def pop_inputs(fun):
    """
    Remove input args from the return value of a function, if present.
    >>> @pop_inputs
    ... def f(a, x=1):
    ...     y = 2
    ...     return locals()
    ...
    >>> f(0)
    {'y': 2}
    """
    param_names = list(signature(fun).parameters)
    @wraps(fun)
    def inner(*pos, **kw):
        result = fun(*pos, **kw)
        [result.pop(key) for key in param_names if key in result]
        return result
    return inner


def pop_key(name):
    """
    Remove named output arg, if present.
    >>> @pop_key('x')
    ... def f():
    ...     x = 1
    ...     y = 2
    ...     return locals()
    ...
    >>> f()
    {'y': 2}
    """
    def deco(fun):
        @wraps(fun)
        def inner(*arg, **kw):
            result = fun(*arg, **kw)
            if name in result:
                result.pop(name)
            return result
        return inner
    return deco


if __name__ == '__main__':
    import doctest
    doctest.testmod()

