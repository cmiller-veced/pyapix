import os
import csv


def split_plus(row):
    sp = row.split()
    if len(sp) == 2:
        return tuple(sp)
    return (sp[0], ' '.join(sp[1:]))


def all_states():
    state_file = "~/local/info/states.csv"
    with open(os.path.expanduser(state_file)) as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader if row][1:]
    return dict([(v,k) for (k,v) in rows])


def cids():
    county_ids = {}
    for row in counties:
        sr = row.split()
        (code, name) = split_plus(row)
        if code.endswith('000'):
            state_name = name
            county_ids[name] = {}
        else:
            (code, county_name) = split_plus(row)
            county_ids[state_name][county_name] = code
    return county_ids


url = 'https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt'
fpath = '~/local/gov/fips.txt'
with open(os.path.expanduser(fpath)) as fh:
    data = fh.readlines()
states = data[16:67]
counties = data[72:]


id2state_name = dict(split_plus(row) for row in states)
id2county_name = dict(split_plus(row) for row in counties)
county_name2id = dict((v,k) for (k,v) in id2county_name.items())
state_name2id = dict((v.title(),k) for (k,v) in id2state_name.items())
county_ids = cids()
abrev2state_name = all_states()
state_name2abrev = dict((v,k) for (k,v) in abrev2state_name.items())

assert not county_name2id == county_ids   # but close.  Eliminate one?

