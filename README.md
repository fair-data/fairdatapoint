[![Build Status](https://travis-ci.org/NLeSC/ODEX-FAIRDataPoint.svg?branch=master)](https://travis-ci.org/NLeSC/ODEX-FAIRDataPoint)
[![DOI](https://zenodo.org/badge/37470907.svg)](https://zenodo.org/badge/latestdoi/37470907)

### FAIR Data Point (FDP)

FDP is a RESTful web service that enables data owners to describe and to expose their datasets (metadata) as well as data users to discover more information about available datasets according to the [FAIR Data Guiding Principles](http://www.force11.org/group/fairgroup/fairprinciples). In particular, FDP addresses the findability or discoverability of data by providing machine-readable descriptions (metadata) at four hierarchical levels:

*FDP->catalogs->datasets->distributions*

FDP software specification can be found [here](https://dtl-fair.atlassian.net/wiki/spaces/FDP/pages/6127622/FAIR+Data+Point+Software+Specification).

FDP has been implemented in:
* [Python](https://github.com/NLeSC/ODEX-FAIRDataPoint/tree/master/fdp-api/python)
* [Java](https://github.com/NLeSC/ODEX-FAIRDataPoint/tree/master/fdp-api/java) (deprecated, use [this](https://github.com/DTL-FAIRData/FAIRDataPoint) version instead)

