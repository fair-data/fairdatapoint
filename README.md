[![Build Status](https://travis-ci.org/NLeSC/ODEX-FAIRDataPoint.svg?branch=master)](https://travis-ci.org/NLeSC/ODEX-FAIRDataPoint)
[![DOI](https://zenodo.org/badge/37470907.svg)](https://zenodo.org/badge/latestdoi/37470907)

### FAIR Data Point (FDP)

FDP is a stand-alone (RESTful) web application that enables data owners to expose their datasets and data users to discover more information about available datasets according to the [FAIR Data Guiding Principles](http://www.force11.org/group/fairgroup/fairprinciples). In particular, FDP addresses the findability or discoverability of data by providing descriptions at four hierarchical levels (metadata):

*FDP->catalogs->datasets->distributions*

Currently, there are two FDP implementations (prototypes) in:
* [Python](https://github.com/NLeSC/ODEX-FAIRDataPoint/tree/master/fdp-api/python)
* [Java](https://github.com/NLeSC/ODEX-FAIRDataPoint/tree/master/fdp-api/java)

FDP software specification can be found [here](https://dtl-fair.atlassian.net/wiki/spaces/FDP/pages/6127622/FAIR+Data+Point+Software+Specification).

**Web API documentation**

Example instance: http://fdp.biotools.nl:8080/

**Programmatic access to FDP-, catalog-, dataset- and distribution-level metadata**

```
curl -iH 'Accept: text/turtle' http://fdp.biotools.nl:8080/fdp
curl -iH 'Accept: text/turtle' http://fdp.biotools.nl:8080/catalog/catalog-01
curl -iH 'Accept: text/turtle' http://fdp.biotools.nl:8080/dataset/breedb
curl -iH 'Accept: text/turtle' http://fdp.biotools.nl:8080/distribution/breedb-sparql
```

Note: FDP supports the following RDF serializations (MIME-types):
* Turtle (text/turtle)
* N-Triples (application/n-triples)
* RDF/XML (application/rdf+xml)
* JSON-LD (application/ld+json)
