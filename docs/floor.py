from functools import singledispatch
import pytest


@singledispatch
def floor(x):
    raise TypeError(f'bad type: {type(x)}')


@floor.register(float)
def _(x):
    return int(x)


@floor.register(int)
def _(x):
    return x


def test_floor():
    with pytest.raises(TypeError):
        floor('a')
    assert floor(1) == 1
    assert floor(1.1) == 1


test_floor()

