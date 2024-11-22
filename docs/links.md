# Interesting Links


### Our motivation

- https://agilemanifesto.org
- https://en.wikipedia.org/wiki/Unix_philosophy
- https://github.com/boto/botocore
- https://www.paulgraham.com
- https://d3js.org

d3js is a javascript library that provides a minimal wrapper around SVG.  If you
understand SVG, d3js will make a lot of sense to you.

- https://aframe.io/docs/1.6.0/introduction/

Aframe is a javascript library around WebGL.


### APIs with OpenAPI doc  (with client here)

- https://www.weather.gov/documentation/services-web-api
- https://api.weather.gov/openapi.json NWS   OpenAPI v 3.0
- https://libretranslate.com/docs/
- https://www.ebi.ac.uk/proteins/api/openapi.json

### APIs with OpenAPI doc  (no client here)

- https://developer.osf.io  open science
- https://raw.githubusercontent.com/BiGCAT-UM/EnsemblOpenAPI/master/swagger.json
- https://github.com/BiGCAT-UM/EnsemblOpenAPI

### Lists of interesting APIs

- https://apis.guru/api-doc/    List of OpenAPI services
- https://github.com/APIs-guru/openapi-directory   good
- https://github.com/public-apis/public-apis   not limited to OpenAPI
- https://any-api.com/      not very useful
- https://www.biorxiv.org/content/10.1101/170274v1.full.pdf
    has list of biology openAPI services

#### The competition

A worthy competitor, but simplistic,  on GitHub, PyPi and readthedocs.
- https://github.com/WxBDM/nwsapy/blob/master/nwsapy/
- https://pypi.org/project/nwsapy/
- https://nwsapy.readthedocs.io/en/latest/index.html

Attempts something similar.  Moribund.
- https://github.com/FKLC/AnyAPI

R package, similar to my thinking
- https://github.com/jonthegeek/anyapi
- https://github.com/jonthegeek/beekeeper

Sophisticated.  More advanced than mine in several aspects.
Excessively complicated in other aspects.
Converts openapi description document to Pydantic models.
- https://github.com/commonism/aiopenapi3


Links to something odd and unreadable.
- https://openapi-core.readthedocs.io/en/latest/extensions.html

No validation.
- https://github.com/wy-z/requests-openapi


### Our tools

- https://github.com/OAI/OpenAPI-Specification
- https://swagger.io/specification/
- https://docs.python.org/3/library/json.html
- https://daringfireball.net/projects/markdown/
- https://github.com
- https://json-schema.org
- https://json-schema.org/understanding-json-schema
- https://developer.mozilla.org/en-US/docs/Web/API/
- python hypothesis for auto-generating data

- https://www.postman.com
- https://pypi.org/project/PyYAML/
- https://jinja.palletsprojects.com/en/3.1.x/
Jinja does for text strings, something like what d3js does for svg.  A minimal
way of inserting data into a fixed string.

### Not our tools

There is nothing wrong with the below tools.  If we have reason, we will use
them.  But it requires justification.  Unfamiliarity with functional programming
in Python is not justification.  "Everyone does it that way." is not
justification.

- https://docs.pydantic.dev/latest/
- https://marshmallow.readthedocs.io/en/stable/
- https://www.attrs.org/en/stable/

These tools tend to make life easy for programmers and their managers.  Most
programmers are familiar with the approach.  It's not too demanding and provides
a simple, rigid interface.  Our goal is to make life easy for the data analyst
or manager who is interested in exploring the interface in real time without
waiting for programmers to define their options for them.

The code we write will demand more from the programmer but will be far more
compact than code written using the above approach.  Also far more flexible.
The data analyst will thank us.


### Potential data sources

- https://documents.worldbank.org/en/publication/documents-reports/api
- https://fred.stlouisfed.org/docs/api/fred/
- https://opensource.fb.com/projects/
- https://developer.x.com/en/docs/x-api

-----------

### Things to watch

- https://htmx.org  Interactivity w/o javascript
- https://opensource.fb.com/projects/ Meta Opensource
- https://jinja.palletsprojects.com/en/3.1.x/templates/
   how to do templates

### Interesting reading

- https://blog.postman.com/what-is-json-schema/
- https://www.semanticarts.com/data-centric-how-big-things-get-done-in-it/
- https://www.semanticarts.com/the-data-centric-revolution-best-practices-and-schools-of-ontology-design/

----------------

- https://stackoverflow.com/questions/2067472/what-is-jsonp-and-why-was-it-created
  jsonp == cross-domain requests
  but CORS is better.
- https://docs.mychem.info/en/latest/doc/chem_annotation_service.html
  a super simple API.  No swagger.
  uses optional jsonp, which is antiquated.


### etc

- https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html
- https://docs.biothings.io/en/latest/
- https://github.com/bio-tools/OpenAPI-Importer     competition ??????
- https://swagger.io/tools/swagger-codegen/  competition.........
- https://github.com/swagger-api/swagger-codegen  the actual code
  still compatible w/ Python 2.


### APIs w/o OpenAPI doc found

- https://open-meteo.com  weather    NO swagger file found
- https://info.arxiv.org/help/api/user-manual.html  no swagger
- https://newton.vercel.app   no swagger.   symbolic math

### etc

- see Trello API.
- google:  nws api client       for useful links


### swagger petstore

We are currently using the Petstore data from the swagger docs.

- https://petstore.swagger.io/v2/swagger.json

### etc

- https://stackoverflow.com/questions/61112684/how-to-subclass-a-dictionary-so-it-supports-generic-type-hints
  Interesting discussion of subclassing builtins.

Denver Open Data.   I wonder.
- https://dataportals.org/portal/denver
- https://opendata-geospatialdenver.hub.arcgis.com
Crap.  Totally non-automatible.

- https://opentelemetry.io/docs/languages/

Walker...
- https://www.datascienceassn.org/resources

Walker's data science laws...
http://www.datascienceassn.org/sites/default/files/Walker%27s%20Data%20Science%20Laws%20by%20Michael%20Walker%20-%20Slides.pdf


https://cmd2.readthedocs.io/en/0.9.9/alternatives.html

### Caveat

jsonschema cannot do everything.


