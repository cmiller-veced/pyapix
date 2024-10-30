
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
        

class common:
    class headers:
        class content_type:
            json = {'Content-Type': 'application/json'}
            form_data = {'Content-Type': 'form-data'}
        class accept:
            json = {'Accept': 'application/json'}

# Another EBI API
# https://www.ebi.ac.uk/interpro/api/static_files/swagger/
