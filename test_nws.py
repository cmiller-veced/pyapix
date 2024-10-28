from functools import lru_cache
from collections import defaultdict
from tools import ( raw_swagger, )
import nother
from nother import NonDictArgs
from test_data_nws import test_parameters
from api_nws import call, _validator, altered_raw_swagger
from info import local


# TODO: clarify messaging.
def validate_and_call():
  try:
    bad_param_but_ok = defaultdict(list)
    good_param_not_ok = defaultdict(list)
    jdoc = raw_swagger(local.swagger.nws)  # TODO: pass flag for deref vs not.?
    paths = altered_raw_swagger(jdoc)['paths']
    for endpoint in paths:
        for verb in paths[endpoint]:
            assert verb in 'get post'
            validator = _validator(endpoint, verb)
            print(endpoint, verb)
            if endpoint in test_parameters:
                things = test_parameters[endpoint]
                for params in things['good']:
                    if not validator.is_valid(params):
                        validator.validate(params)
                    print('   ok good valid', params)
                    response = call(endpoint, verb, params)
                    if not response.is_success:
                        good_param_not_ok[(endpoint, verb)].append(params)
                        raise ValidDataBadResponse(params)
                    if response.is_success:
                        print('   ok good call')
                for params in things['bad']:
                    assert not validator.is_valid(params)
                    print('   ok bad NOT valid', params)
                    try:
                        # TODO: re-extract prepped args.   ?????
                        # NO.
                        # Maybe.
                        # But first get accustomed to debugging as-is.
                        # Should have better visibility there.
                        response = call(endpoint, verb, params)
                    except NonDictArgs:
                        break
                    if response.is_success:
                        bad_param_but_ok[(endpoint, verb)].append(params)
  finally:
    bad_param_but_ok = dict(bad_param_but_ok)
    good_param_not_ok = dict(good_param_not_ok)
    globals().update(locals())


def current_alerts(area='CO', zone='COZ040', event='Red Flag Warning'):
  try:
    denver_zone = 'COZ040'
    params = dict(zone=zone)
    params = dict(area=area, event=event)
    params = dict(area=area)
    endpoint, verb = '/alerts/active', 'get'
    response = call(endpoint, verb, params).json()
    feats = response['features']    # The interesting part
    return feats
  finally:
    cp = [a['properties'] for a in feats]
    for a in cp:
        az = a['affectedZones']
        ac = a['category']
        ae = a['event']
        ah = a['headline']
        ad = a['description']
        ax = a['areaDesc']
        ae = a['event']
        ae = a['event']
        print(ah)
        print('='*55)
        print(ad)
        print('='*55)
        print(' ' + ax.replace(';', '\n'))
        print()
        print()
    globals().update(locals())
#     return response['features']    # The interesting part
#     return response['type']        # 'FeatureCollection'
#     return response['title']       # string
#     return response['@context']    # list of stuff
#     return response['updated']     # timestamp


# Fetch a data set suitable for a pandas dataframe.
# ############################################################################
import pandas


def nws_series():
  try:
    """ Get a series of observations suitable for putting in a pandas DF,
    and then a jupyter notebook.
    """
    # Data
    ep1 = '/stations/{stationId}/observations'
    stationId = 'KRCM'   # OK
    stationId = 'CO100'   # OK
    params = {                                # OK
        'stationId': stationId, 
        'start': '2024-09-22T23:59:59+00:00', 
        'end':   '2024-09-23T23:59:59+00:00', 
        'limit':   50,
    }
    validator = _validator(ep1, 'get')
    assert validator.is_valid(params)

    response = call(ep1, 'get', params)
    assert response.status_code == 200

    # Extract desired data from response.
    final = []
    feats = response.json()['features']
    for ft in feats: 
        pt = ft['properties']
        for key in [ '@id', '@type', 'elevation', 'station', 'rawMessage', 'icon', 'presentWeather', 'cloudLayers', 'textDescription', ]:
            pt.pop(key)
        for key in pt:
            if type(pt[key]) is dict:
                pt[key] = pt[key]['value']
        final.append(pt)

    # Convert to dataframe.
    df = pandas.DataFrame(final)
    assert df.shape[1] == 15
    return df
  finally:
    globals().update(locals())


if __name__ == '__main__':
    ca = current_alerts()
    validate_and_call()
#    nws_series()

