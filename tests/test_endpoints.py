import pytest

from fdp.fdp import app, initGraph


fdp_post_data = '''
@prefix dbp: <http://dbpedia.org/resource/> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcmitype: <http://purl.org/dc/dcmitype/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix lang: <http://id.loc.gov/vocabulary/iso639-1/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://0.0.0.0:8080/fdp> a dcterms:Agent ;
    rdfs:label "FAIR Data Point service of Plant Breeding group at Wageningen University and Research."^^xsd:string ;
    dcterms:description "This service provides machine-readable descriptions about available datasets (metadata)."^^xsd:string ;
    dcterms:hasPart <http://0.0.0.0:8080/catalog/pbg-ld> ;
    dcterms:hasVersion "0.1"^^xsd:string ;
    dcterms:identifier "PBR-WUR"^^xsd:string ;
    dcterms:issued "2019-04-09"^^xsd:date ;
    dcterms:language lang:en ;
    dcterms:modified "2019-04-09"^^xsd:date ;
    dcterms:publisher <http://orcid.org/0000-0003-1711-7961> ;
    dcterms:title "FAIR Data Point service of Plant Breeding group at Wageningen University and Research."^^xsd:string ;
    rdfs:seeAlso <http://0.0.0.0:8080/catalog/pbg-ld> .
'''

catalog01_post_data = '''
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix fdp: <http://rdf.biosemantics.org/ontologies/fdp-o#> .
@prefix dbp: <http://dbpedia.org/resource/> .

<http://0.0.0.0:8080/catalog/catalog-01> a dcat:Catalog ;
    dct:title "Title" ;
    dct:hasVersion "1.0" ;
    dct:publisher <http://orcid.org/0000-0002-4368-8058> ;
    dct:isPartOf <fdp> ;
    fdp:metadataIdentifier <http://example.org/metadataID> ;
    fdp:metadataIssued "2016-10-27"^^xsd:date ;
    fdp:metadataModified "2016-10-27"^^xsd:date ;
    dcat:dataset <dataset/breedb> ;
    dcat:themeTaxonomy dbp:Breeding .
'''

catalog02_post_data = '''
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix fdp: <http://rdf.biosemantics.org/ontologies/fdp-o#> .
@prefix dbp: <http://dbpedia.org/resource/> .

<http://0.0.0.0:8080/catalog/catalog-02> a dcat:Catalog ;
    dct:title "Title" ;
    dct:hasVersion "1.0" ;
    dct:publisher <http://orcid.org/0000-0002-4368-8058> ;
    dct:isPartOf <fdp> ;
    fdp:metadataIdentifier <http://example.org/metadataID> ;
    fdp:metadataIssued "2016-10-27"^^xsd:date ;
    fdp:metadataModified "2016-10-27"^^xsd:date ;
    dcat:dataset <dataset/breedb> ;
    dcat:themeTaxonomy dbp:Breeding .
'''

dataset01_post_data = '''
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix fdp: <http://rdf.biosemantics.org/ontologies/fdp-o#> .
@prefix dbp: <http://dbpedia.org/resource/> .

<http://0.0.0.0:8080/dataset/breedb> a dcat:Dataset ;
    dct:title "BreeDB tomato passport data"^^xsd:string ;
    dct:publisher <http://orcid.org/0000-0002-4368-8058> ;
    dct:hasVersion "1.0"^^xsd:string ;
    dct:isPartOf <catalog/catalog-01> ;
    fdp:metadataIdentifier <http://example.org/metadataID> ;
    fdp:metadataIssued "2016-10-27"^^xsd:date ;
    fdp:metadataModified "2016-10-27"^^xsd:date ;
    dcat:distribution <distribution/breedb-sparql>,
        <distribution/breedb-sqldump> ;
    dcat:theme dbp:Plant_breeding .
'''

dataset02_post_data = '''
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix fdp: <http://rdf.biosemantics.org/ontologies/fdp-o#> .
@prefix dbp: <http://dbpedia.org/resource/> .

<http://0.0.0.0:8080/dataset/dataset02> a dcat:Dataset ;
    dct:title "BreeDB tomato passport data"^^xsd:string ;
    dct:publisher <http://orcid.org/0000-0002-4368-8058> ;
    dct:hasVersion "1.0"^^xsd:string ;
    dct:isPartOf <catalog/catalog-01> ;
    fdp:metadataIdentifier <http://example.org/metadataID> ;
    fdp:metadataIssued "2016-10-27"^^xsd:date ;
    fdp:metadataModified "2016-10-27"^^xsd:date ;
    dcat:distribution <distribution/breedb-sparql>,
        <distribution/breedb-sqldump> ;
    dcat:theme dbp:Plant_breeding .
'''

dist01_post_data = '''
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix fdp: <http://rdf.biosemantics.org/ontologies/fdp-o#> .
@prefix dbp: <http://dbpedia.org/resource/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix lang: <http://id.loc.gov/vocabulary/iso639-1/> .

<http://0.0.0.0:8080/distribution/breedb-sparql> a dcat:Distribution ;
    dct:title "SPARQL endpoint for BreeDB tomato passport data"^^xsd:string ;
    dct:license <http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0> ;
    dct:hasVersion "1.0"^^xsd:string ;
    dct:isPartOf <dataset/breedb> ;
    fdp:metadataIdentifier <http://example.org/metadataID> ;
    fdp:metadataIssued "2016-10-27"^^xsd:date ;
    fdp:metadataModified "2016-10-27"^^xsd:date ;
    dcat:mediaType "application/n-triples"^^xsd:string,
        "application/rdf+xml"^^xsd:string ;
    dcat:accessURL <http://virtuoso.biotools.nl:8888/sparql> .
'''

dist02_post_data = '''
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix fdp: <http://rdf.biosemantics.org/ontologies/fdp-o#> .
@prefix dbp: <http://dbpedia.org/resource/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix lang: <http://id.loc.gov/vocabulary/iso639-1/> .

<http://0.0.0.0:8080/distribution/dist02> a dcat:Distribution ;
    dct:title "SPARQL endpoint for BreeDB tomato passport data"^^xsd:string ;
    dct:license <http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0> ;
    dct:hasVersion "1.0"^^xsd:string ;
    dct:isPartOf <dataset/breedb> ;
    fdp:metadataIdentifier <http://example.org/metadataID> ;
    fdp:metadataIssued "2016-10-27"^^xsd:date ;
    fdp:metadataModified "2016-10-27"^^xsd:date ;
    dcat:mediaType "application/n-triples"^^xsd:string,
        "application/rdf+xml"^^xsd:string ;
    dcat:accessURL <http://virtuoso.biotools.nl:8888/sparql> .
'''


def setup_module(module):
    '''Initialize in-memory graph with minimal data.'''
    initGraph(host='0.0.0.0', port=8080, dataFile=None, endpoint='http://0.0.0.0:8890/sparql')


@pytest.fixture
def client():
    '''Build http client'''
    with app.test_client() as client:
        yield client
    # Nothing to do, no connections to close.


def test_fdp(client):
    """Testing post and get to fdp"""
    rv = client.post('/fdp', data=fdp_post_data)
    assert rv.status_code == 200
    assert 'message' in rv.json
    assert rv.json['message'] == 'Ok'

    rv = client.get('/fdp')
    assert rv.status_code == 200
    # TODO: validate rv.data?

    rv = client.delete('/fdp')
    assert rv.status_code == 405
    assert 'message' in rv.json
    assert rv.json['message'] == 'Method Not Allowed'


def test_catalog(client):
    """Testing post and get to catalog"""
    rv = client.post('/catalog/', data=catalog01_post_data)
    assert rv.status_code == 200
    assert 'message' in rv.json
    assert rv.json['message'] == 'Ok'

    rv = client.post('/catalog/', data=catalog02_post_data)
    assert rv.status_code == 200
    assert 'message' in rv.json
    assert rv.json['message'] == 'Ok'

    rv = client.get('/catalog/')
    assert rv.status_code == 200
    # TODO: validate rv.data?
    # TODO: validate return list as JSON structure

    rv = client.get('/catalog/catalog-01')
    assert rv.status_code == 200
    # TODO: validate response

    rv = client.get('/catalog/catalog-02')
    assert rv.status_code == 200
    # TODO: validate response

    rv = client.delete('/catalog/catalog-01')
    assert rv.status_code == 200
    assert 'message' in rv.json
    assert rv.json['message'] == 'Ok'

    rv = client.get('/catalog/catalog-01')
    assert rv.status_code == 404
    assert 'message' in rv.json
    assert rv.json['message'] == 'Not Found'

    rv = client.get('/catalog/')
    assert rv.status_code == 200
    # TODO: validate rv.data -- catalog-01 should not be listed


def test_dataset(client):
    """Testing post and get to dataset"""
    rv = client.post('/dataset/', data=dataset01_post_data)
    assert rv.status_code == 200
    assert rv.json['message'] == 'Ok'

    rv = client.post('/dataset/', data=dataset02_post_data)
    assert rv.status_code == 200
    assert rv.json['message'] == 'Ok'

    rv = client.get('/dataset/')
    assert rv.status_code == 200
    # TODO: validate rv.data?
    # TODO: validate return list as JSON structure

    rv = client.get('/dataset/breedb')
    assert rv.status_code == 200
    # TODO: validate response

    rv = client.get('/dataset/dataset02')
    assert rv.status_code == 200
    # TODO: validate response

    rv = client.delete('/dataset/breedb')
    assert rv.status_code == 200
    assert 'message' in rv.json
    assert rv.json['message'] == 'Ok'

    rv = client.get('/dataset/breedb')
    assert rv.status_code == 404
    assert 'message' in rv.json
    assert rv.json['message'] == 'Not Found'

    rv = client.get('/dataset/')
    assert rv.status_code == 200
    # TODO: validate rv.data -- datased breedb should not be listed


def test_distribution(client):
    """Testing post and get to distribution"""

    rv = client.post('/distribution/', data=dist01_post_data)
    assert rv.status_code == 200
    assert rv.json['message'] == 'Ok'

    rv = client.post('/distribution/', data=dist02_post_data)
    assert rv.status_code == 200
    assert rv.json['message'] == 'Ok'

    rv = client.get('/distribution/')
    assert rv.status_code == 200
    # TODO: validate rv.data?
    # TODO: validate return list as JSON structure

    rv = client.get('/distribution/breedb-sparql')
    assert rv.status_code == 200
    # TODO: validate response

    rv = client.get('/distribution/dist02')
    assert rv.status_code == 200
    # TODO: validate response

    rv = client.delete('/distribution/dist02')
    assert rv.status_code == 200
    assert 'message' in rv.json
    assert rv.json['message'] == 'Ok'

    rv = client.get('/distribution/dist02')
    assert rv.status_code == 404
    assert 'message' in rv.json
    assert rv.json['message'] == 'Not Found'

    rv = client.get('/distribution/')
    assert rv.status_code == 200
    # TODO: validate rv.data -- catalog-01 should not be listed
