# FAIR Data Point (FDP)

[![PyPI](https://img.shields.io/pypi/v/fairdatapoint)](https://pypi.org/project/fairdatapoint/)
[![Docker Image Version (latest by date)](https://img.shields.io/docker/v/nlesc/fairdatapoint?label=Docker)](https://hub.docker.com/r/nlesc/fairdatapoint)
[![DOI](https://zenodo.org/badge/37470907.svg)](https://zenodo.org/badge/latestdoi/37470907)
[![Research Software Directory](https://img.shields.io/badge/RSD-FAIRDataPoint-red)](https://research-software.nl/software/fairdatapoint)
[![Build_Test](https://github.com/fair-data/fairdatapoint/actions/workflows/build_test.yml/badge.svg)](https://github.com/fair-data/fairdatapoint/actions/workflows/build_test.yml)
[![Coverage Status](https://coveralls.io/repos/github/fair-data/fairdatapoint/badge.svg?branch=master)](https://coveralls.io/github/fair-data/fairdatapoint?branch=master)

> 
> ⚠️ **Warning**
>
> This repo is **no longer maintained**.
>
> You could **switch to the [Java implementation](https://github.com/DTL-FAIRData/FAIRDataPoint)**.
> 


## Overview
Python implementation of FAIR Data Point.

FDP is a RESTful web service that enables data owners to describe and to expose their datasets (metadata) as well as data users to discover more information about available datasets according to the [FAIR Data Guiding Principles](http://www.force11.org/group/fairgroup/fairprinciples). In particular, FDP addresses the findability or discoverability of data by providing machine-readable descriptions (metadata) at four hierarchical levels:

*FDP -> catalogs -> datasets -> distributions*

FDP software specification can be found [here](https://github.com/FAIRDataTeam/FAIRDataPoint-Spec/blob/master/spec.md).
Other implementations are also available, e.g. [Java implementation](https://github.com/DTL-FAIRData/FAIRDataPoint)

## Installation

To install FDP, do

From pypi
```bash
pip install fairdatapoint
```

Or from this repo, but note that the in-development version might be unstable,
```bash
git clone https://github.com/fair-data/fairdatapoint.git
cd fairdatapoint
pip install .
```

## Running
```bash
fdp-run localhost 80
```

The [Swagger UI](https://swagger.io/tools/swagger-ui/) is enabled for FDP service, and you can have a try by visiting http://localhost.

## Unit testing
Run tests (including coverage) with:

```bash
pip install .[tests]
pytest
```

## Deploy with Docker

Check [fairdatapoint-service](https://github.com/CunliangGeng/fairdatapoint-service).

## Deploy without Docker

Before deploying FDP, it's necessary to first have a running SPARQL database which can be used to store metadata.

```
pip install fairdatapoint

# fdp-run <host> <port> --db=<sparql-endpoint>
# Let's assume your <host> is 'example.com' and <sparql-endpoint> is 'http://example.com/sparql', then
fdp-run example.com 80 --db='http://example.com/sparql'
```

## Web API documentation

FAIR Data Point (FDP) exposes the following endpoints (URL paths):

| Endpoint |  GET  | POST |  PUT | DELETE     |
|--------------|:--------------:|:-----------------:|:--------------:|:--------------:
| fdp | Output fdp metadata | Create new fdp metadata | Update fdp metadata | Not Allowed |
| catalog     | Output all catalog IDs   | Create new catalog metadata| Not Allowed | Not Allowed |
| dataset     | Output all dataset IDs   | Create new dataset metadata| Not Allowed | Not Allowed |
| distribution  | Output all distribution IDs  | Create new distribution metadata| Not Allowed | Not Allowed |
| catalog/\<catalogID\> | Output \<catalogID\> metadata | Not Allowed | Update \<catalogID\> metadata | Remove \<catalogID\> metadata |
| dataset/\<datasetID\> | Output \<datasetID\> metadata | Not Allowed | Update \<datasetID\> metadata | Remove \<datasetID\> metadata |
| distribution/\<distributionID\> | Output \<distributionID\> metadata | Not Allowed | Update \<distributionID\> metadata | Remove \<distributionID\> metadata |


### Access endpoints to request metadata programmatically

FDP: `curl -iH 'Accept: text/turtle' [BASE URL]/fdp`

Catalog: `curl -iH 'Accept: text/turtle' [BASE URL]/catalog/catalog01`

Dataset: `curl -iH 'Accept: text/turtle' [BASE URL]/dataset/dataset01`

Distribution: `curl -iH 'Accept: text/turtle' [BASE URL]/distribution/dist01`

### FDP supports the following RDF serializations (MIME-types):
* Turtle: `text/turtle`
* N-Triples: `application/n-triples`
* N3: `text/n3`
* RDF/XML: `application/rdf+xml`
* JSON-LD: `application/ld+json`


## Issues and Contributing
If you have questions or find a bug, please report the issue in the
[Github issue channel](https://github.com/fair-data/fairdatapoint/issues).

If you want to contribute to the development of FDP, have a look at the
[contribution guidelines](CONTRIBUTING.rst).
