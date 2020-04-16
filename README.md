[![DOI](https://zenodo.org/badge/37470907.svg)](https://zenodo.org/badge/latestdoi/37470907)
[![Build Status](https://travis-ci.org/c-martinez/FAIRDataPoint.svg?branch=dev)](https://travis-ci.org/c-martinez/FAIRDataPoint)
[![Coverage Status](https://coveralls.io/repos/github/c-martinez/FAIRDataPoint/badge.svg)](https://coveralls.io/github/c-martinez/FAIRDataPoint)


### FAIR Data Point (FDP)

Python implementation of FAIR Data Point.

FDP is a RESTful web service that enables data owners to describe and to expose their datasets (metadata) as well as data users to discover more information about available datasets according to the [FAIR Data Guiding Principles](http://www.force11.org/group/fairgroup/fairprinciples). In particular, FDP addresses the findability or discoverability of data by providing machine-readable descriptions (metadata) at four hierarchical levels:

*FDP->catalogs->datasets->distributions*

FDP software specification can be found [here](https://dtl-fair.atlassian.net/wiki/spaces/FDP/pages/6127622/FAIR+Data+Point+Software+Specification).

FDP has been implemented in:
* [Python](https://github.com/NLeSC/ODEX-FAIRDataPoint/)
* [Java](https://github.com/DTL-FAIRData/FAIRDataPoint)

## Installation
------------

To install fdp, do:

```bash
git clone https://github.com/NLeSC/ODEX-FAIRDataPoint.git
cd ODEX-FAIRDataPoint
pip install .
```
TODO: register on pypi and change this to `pip install fairdatapoint`

## Running
```bash
fdp-run samples/plant_breeding_group.ttl
```

Then visit from your browser: http://localhost:8080/

## Unit testing
Run tests (including coverage) with:

```bash
python setup.py test
```

TODO: Include a link to your project's full documentation here.

## Contributing

If you want to contribute to the development of FAIR Data Point,
have a look at the [contribution guidelines](CONTRIBUTING.rst).

## License

Copyright (c) 2019,

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Deploy with Docker
TODO: update docker deployment

`docker run -p 8080:8080 -d nlesc/odex-fairdatapoint`

## Deploy without Docker
TODO: update this section

Clone this repo.

```
git clone https://github.com/NLeSC/ODEX-FAIRDataPoint.git
cd ODEX-FAIRDataPoint/fdp-api/python
```

Install FDP into ENV.

```
python -m venv ENV
source /ENV/bin/activate

make install
# make clean # removes files from doc dir (except swagger.json)
```

Edit metadata in `config.ini`.

```
# in development
make serve-dev # with default HOST=127.0.0.1:8080
make test
# in production
make -e serve-prod HOST=example.com
```

**Web API documentation**

Base URL: `http://127.0.0.1:8080`

**Access endpoints to request metadata programmatically**

FDP: `curl -iH 'Accept: text/turtle' [BASE URL]/fdp`

Catalog: `curl -iH 'Accept: text/turtle' [BASE URL]/catalog/catalog-01`

Dataset: `curl -iH 'Accept: text/turtle' [BASE URL]/dataset/breedb`

Distribution: `curl -iH 'Accept: text/turtle' [BASE URL]/distribution/breedb-sparql`

Note: FDP supports the following RDF serializations (MIME-types):
* Turtle: `text/turtle`
* N-Triples: `application/n-triples`
* RDF/XML: `application/rdf+xml`
* JSON-LD: `application/ld+json`


## FAIR Data Point specification

FAIR Data Point (FDP) exposes the following endpoints (URL paths):

| Endpoints | Description |
| -- | -- |
| [ /, /doc, /doc/ ]   | Redirects to the API documentation |
| /fdp                 | Returns FDP metadata |
| /catalog/{catalogID} | Returns catalog metadata (default: catalog-01) |
| /dataset/{datasetID} | Returns dataset metadata (default: breedb) |
| /distribution/{distributionID} | Returns distribution metadata (default: breedb-sparql) |

This services makes use of:
 - [Data Catalog Vocabulary](http://www.w3.org/TR/vocab-dcat/)
 - [Dublin Core Metadata Terms](http://dublincore.org/documents/dcmi-terms/)
 - [DBpedia](http://dbpedia.org/resource/)

 ## Credits

 This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [NLeSC/python-template](https://github.com/NLeSC/python-template).
