"""
Use a NWS postman file.
# Below url is exportable & downloadable to json if logged in to postman.
url = 'https://www.postman.com/api-evangelist/national-oceanic-and-atmospheric-administration-noaa/documentation/9eu7ygi/weather-gov'
BUT
The thing above has NO parameters!
Fooeey!

# But this has parameters?
https://github.com/aisabel/PetStore-Postman
Looks like it does.
It has collection AND environment.
But is PUNY.

btw.  Postman is acting like assholes.  People are switching to Bruno.
https://www.usebruno.com
enshitification
Postman requires storing credentials in the cloud, apparently.
Because Postman now requires a cloud account.

"""
import os
from pyapix.tool.tools import parsed_file_or_url
from pyapix.tool import working_with_postman as wp
from pyapix.tool.working_with_postman import (
    is_request, fetch_thing,
)

def pm_files():
    files = ['~/local/Weather.gov.postman_collection.json']
    return [os.path.expanduser(f) for f in files]


def test_fetch_thing():
  try:
    jdoc = parsed_file_or_url(pm_files()[0])
    names = [
        'zones',
        '{type}',
        '{zone Id}',
        '/zones/:type/:zoneId/forecast',
        ]
    assert fetch_thing(jdoc) == jdoc
    zi = fetch_thing(jdoc, *names[:-1])
    zr = fetch_thing(jdoc, *names)
    assert str(zr) in str(zi)
    zrr = zr['request']
    assert list(zi) == ['name', 'item']
    assert list(zr) == ['name', 'request']
    assert list(zrr) == ['method', 'header', 'url', 'description']
    assert is_request(zr)
    assert not is_request(zi)
  finally:
    globals().update(locals())

