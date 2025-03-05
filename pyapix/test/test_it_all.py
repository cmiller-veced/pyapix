import doctest

import test_petstore
from pyapix.tool import working_with_postman
from pyapix.tool import do_postman_osdu
from pyapix.tool import do_postman_nws
from pyapix.osdu import crs_api
 

def test_it():
    dps = [do_postman_nws, do_postman_osdu]
    mods = [working_with_postman, crs_api] + dps

    for mod in mods:
        doctest.testmod(mod)

    for mod in dps:
        working_with_postman.check_do_item(mod.pm_files)
        mod.test_fetch_thing()

    working_with_postman.test_environment_update()

    crs_api.inspect_swagger()
    crs_api.inspect_postman()
    crs_api.test_crs_conversion()

#     test_petstore.test_seq()


test_it()
