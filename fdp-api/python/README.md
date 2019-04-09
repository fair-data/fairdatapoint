**Deploy with Docker**

`docker run -p 8080:8080 -d nlesc/odex-fairdatapoint`

**Deploy without Docker**

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

