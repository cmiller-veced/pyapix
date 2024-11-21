"""
Write code to find the differences between two json docs.
"""


def test_diff():
    jd1 = dict(a1=dict(a2='a', b2='b', c2='c'))
    jd2 = dict(a1=dict(a2='a', b2=2))

    assert jd1 - jd2 == {'a1': {'b2': 'b', 'c2': 'c'}}
    assert jd2 - jd1 == {'a1': {'b2': 2}}


