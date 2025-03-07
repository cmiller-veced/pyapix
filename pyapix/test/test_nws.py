# Copyright (c) 2024-2025 Cary Miller
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
# THIS SOFTWARE.

from functools import lru_cache
from collections import defaultdict
import pytest

from pyapix.tool.tools import parsed_file_or_url
from pyapix.tool.api_tools import NonDictArgs
from pyapix.client.nws import call, _validator, altered_raw_swagger, config

# TODO: consider making call behave like _validator.
# The behavior of the two is currently maybe surprising / inconsistent.
# but the code is currently minimal.
# but the change will be a one-liner.

pfile = '../test_data/nws.yaml'
test_parameters = parsed_file_or_url(pfile)['test_parameters']
sfile = '../test_data/nws_sequence.yaml'
sdata = parsed_file_or_url(sfile)



# TODO: clarify messaging.
def test_validate_and_call():
  try:
    bad_param_but_ok = defaultdict(list)
    good_param_not_ok = defaultdict(list)
    jdoc = parsed_file_or_url(config.swagger_path)  # TODO: pass flag for deref vs not.?
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
                if endpoint == '/stations/{stationId}/observations':
                    break
                break  # before bad
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


def demo_current_alerts(area='CO', zone='COZ040', event='Red Flag Warning'):
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


def demo_nws_series():
  try:
    """ Get a series of observations suitable for putting in a pandas DF,
    and then a jupyter notebook.
    """
    import pandas
    # Data
    endpoint = '/stations/{stationId}/observations'
    stationId = 'KRCM'   # OK
    stationId = 'CO100'   # OK
    params = {                                # OK
        'stationId': stationId, 
#         'start': '2024-11-13:59:00+00:00', 
#         'end': '2024-11-14:59:00+00:00', 
        'limit':   50,
    }
    # Seems it may require recent timestamps.
    validator = _validator(endpoint, 'get')
    assert validator.is_valid(params)

    response = call(endpoint, 'get', params)
    assert response.status_code == 200

    # Extract desired data from response.
    final = []
    feats = response.json()['features']
    assert feats
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
#    assert df.shape[0] > 10
    assert df.shape[1] == 15
    return df
  finally:
    globals().update(locals())


def test_current_alerts():
    # Because returning a value from a test generates a pytest warning.
    demo_current_alerts()


def test_nws_series():
    # Because returning a value from a test generates a pytest warning.
    demo_nws_series()


from pyapix.client.nws import call, _validator, altered_raw_swagger, config
from pyapix.client import nws
from pyapix.tool.peemish import run_seq, sequence_creator
from pyapix.tool import peemish
from pyapix.osdu.working_with_postman import Environment

sdata = parsed_file_or_url(sfile)

def test_seq():
    create_sequence = sequence_creator(nws.service)
    cs = create_sequence(sdata['nws_sequence'])

    env = Environment()     # Update the env with sdata
    env.collection['N'] = sdata['N']
    run_seq(cs, env)
    print(env.current)

    # exploration below
    response = peemish.response
    prj = peemish.response.json()
    feats = prj['features']
    for feat in feats:
        props = feat['properties']
        temp = feat['properties']['temperature']['value']
    globals().update(locals())
#     prf = peemish.response.json()['features']
#     for feat in prf:
#         fp = feat['properties']
#         # contains different zones; fireZone, forecastZone, etc.
#         forecast = fp['forecast']
#         county = fp['county']
#         fire = fp['fireWeatherZone']
#         observation = fp['@id']
# 
#     fts = set(f['properties']['@type'] for f in prf)
#     pros = peemish.response.json()['observationStations']
#     for station in pros: pass
#     stations = dict(
#         station=station,
#         forecast=forecast,
#         county=county,
#         fire=fire,
#         observation=observation
#     )
    globals().update(locals())


