import pytest
import api_requiring_auth

validator = api_requiring_auth._validator
call = api_requiring_auth.call


def test_auth():
    endpoint, verb = '/some/endpoint', 'verb'
    args = dict(foo=2)
    auth_info = dict(user='u', password='p')
    with pytest.raises(Exception):
        call(endpoint, verb, args)

    auth_args = altered(args, auth_args)
    response = call(endpoint, verb, auth_args)
    assert response.is_success

