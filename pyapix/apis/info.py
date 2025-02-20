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


class local:
    class swagger:
        petstore = '~/local/petstore/swagger.json'
        nws = '~/local/nws/openapi.json'
        protein = '~/local/ebi/protein_openapi.json'
        libre =  '~/local/libretranslate/openapi.json'
        obis =  '~/local/obis/obis_v3.yml'
        worms =  '~/local/worms/openapi.yaml'
    class api_base:
        petstore = 'https://petstore.swagger.io/v2'
        nws = 'https://api.weather.gov'
        protein = 'https://www.ebi.ac.uk/proteins/api'
        libre = 'http://localhost:5000'
        obis = 'https://api.obis.org/v3'
        worms = 'https://www.marinespecies.org/rest'

class remote:
    class swagger:
        petstore = 'https://petstore.swagger.io/v2/swagger.json'
        nws = 'https://api.weather.gov/openapi.json'
        interpro = 'https://www.ebi.ac.uk/interpro/api/static_files/interpro7-swagger.yml'
#        protein = 'cannot find it'
#        libre = 'https://libretranslate.com/docs/spec'
#        This is it.  Loads in browser w/o incident but not programatically.
        obis = 'https://api.obis.org/obis_v3.yml'
        worms = 'https://www.marinespecies.org/rest/api-docs/openapi.yaml'
        

class common:
    class headers:
        class content_type:
            json = {'Content-Type': 'application/json'}
            form_data = {'Content-Type': 'form-data'}
        class accept:
            json = {'Accept': 'application/json'}


