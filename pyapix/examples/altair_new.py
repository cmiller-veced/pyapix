"""
Plot data for every US county.
#https://altair-viz.github.io/user_guide/transform/lookup.html#user-guide-lookup-transform
"""
import random

import altair as alt
from vega_datasets import data

from pyapix.client.nws import service
from county_codes import ( county_ids, abrev2state_name, )

counties = alt.topo_feature(data.us_10m.url, 'counties')
ud = data('unemployment')
stop_words = 'Eastern Western Central Northern Southern County'
stop_words = stop_words.split()


def find_active_alert():
    """Call /alerts/active on random states until an alert is found.
    """
    states = list(abrev2state_name)
    while True:
        state = random.choice(states)
        print(state)
        if state not in abrev2state_name:
            continue
        state_long = abrev2state_name[state]
        params = {'area': [state]}
        response = service.call('/alerts/active', 'get', params)
        rj = response.json()
        if (not 'features' in rj) or (not rj['features']):
            continue  # to next random state.
        cid_set = set()
        feats = rj['features']
        for feat in feats:
            props = feat['properties']
            event = feat['properties']['event']
            ad = feat['properties']['areaDesc']
            ad_parts = ad.split(';')
            for part in ad_parts:
                for word in stop_words:
                    if word in part:
                        part = part.replace(word, '')
                part = part.strip()
                key = f'{part} County'
                if state_long not in county_ids:
                    continue
                if key in county_ids[state_long]:
                    cid = county_ids[state_long][key]   # eg '16059'
                    print('  ', cid)
                    cid_set.add(cid)
            print(state, event, ad)
        if not cid_set:
            continue
        print(cid_set)
        print()
        break
    return cid_set


def make_chart():
    cid_set = find_active_alert()       # a list of county IDs.

    for (index, row) in ud.iterrows():
        rid = str(int(row['id']))
        if rid in cid_set:
            ud.at[index, 'rate'] = 0.99

    chart = alt.Chart(counties).mark_geoshape().encode(
        color='rate:Q'
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(ud, 'id', ['rate'])
    ).properties(
        projection={'type': 'albersUsa'},
        width=500, height=300
    )
    chart.save('counties.html')   # visible in the browser


def demo(n=3):
    """Run it multiple times to get alerts in a few random states.
    """
    for _ in range(n):
        make_chart()

