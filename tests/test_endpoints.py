import pytest

from fdp.fdp import create_app

@pytest.fixture(scope='class',
                params=[None, 'http://0.0.0.0:8890/sparql'],
                ids =['Memory Store', 'Persistent Store'])
def client(request):
    '''Build http client'''
    app = create_app(host='0.0.0.0', port=80, graph_endpoint=request.param)
    with app.test_client() as client:
        yield client

# to make sure creating a new store when calling client
@pytest.fixture(scope='function', params=[None], ids =['Memory Store'])
def client_new_store(request):
    app = create_app(host='0.0.0.0', port=80, graph_endpoint=request.param)
    with app.test_client() as client:
        yield client


class TestBaseEndpointTests:
    '''All implementations fo FDP should work for all endpoints.'''

    # datadir fixture provided via pytest-datadir-ng
    def test_fdp(self, client, datadir):
        """Testing post, get and put to fdp"""
        rv = client.post('/fdp', data=datadir['fdp.ttl'])
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client.get('/fdp')
        assert rv.status_code == 200
        assert 'Allow' in rv.headers
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'text/turtle'
        assert b'hasVersion "0.1"' in rv.data
        assert b'metadataIssued "2019-04-09T10:01:00"^^xsd:dateTime' in rv.data

        rv = client.put('/fdp', data=datadir['fdp_update.ttl'])
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client.get('/fdp')
        assert rv.status_code == 200
        assert b'hasVersion "0.2"' in rv.data

        rv = client.delete('/fdp')
        assert rv.status_code == 405

    def test_fdp_invalid(self, client, datadir):
        """Test invalid metadata to fdp layer"""

        rv = client.post('/fdp', data=datadir['fdp_invalid_missingRDFtype.ttl'])
        assert rv.status_code == 405
        assert 'message' in rv.json
        assert 'Not found subject with required RDF type' in rv.json['message']

        rv = client.post('/fdp', data=datadir['fdp_invalid_wrongRDFtype.ttl'])
        assert rv.status_code == 405
        assert 'message' in rv.json
        assert 'Not found subject with required RDF type' in rv.json['message']

        rv = client.post('/fdp', data=datadir['fdp_invalid_blank.ttl'])
        assert rv.status_code == 405
        assert 'message' in rv.json
        assert 'Not found subject with required RDF type' in rv.json['message']

        rv = client.post('/fdp', data=datadir['fdp_invalid_missingRequired.ttl'])
        assert rv.status_code == 405
        assert 'message' in rv.json
        assert 'Validation Report\nConforms: False\nResults (8)' in rv.json['message']

        rv = client.post('/fdp', data=datadir['fdp_invalid_unknownTerms.ttl'])
        assert rv.status_code == 405
        assert 'message' in rv.json
        assert 'Validation Report\nConforms: False\nResults (2)' in rv.json['message']

        rv = client.post('/fdp', data=datadir['fdp_invalid_2foucsNodes.ttl'])
        assert rv.status_code == 405
        assert 'message' in rv.json
        assert 'FDP layer allows only one subject' in rv.json['message']

        rv = client.post('/fdp', data=datadir['fdp_invalid_mixedMetadata.ttl'])
        assert rv.status_code == 405
        assert 'message' in rv.json
        assert 'Not allowed RDF type for layer FDP' in rv.json['message']

    def test_catalog(self, client, datadir):
        """Testing post, get, put and delete to catalog"""
        rv = client.post('/catalog', data=datadir['catalog01.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.post('/catalog', data=datadir['catalog02.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.get('/catalog')
        assert rv.status_code == 200
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'text/plain'
        assert b'catalog01' in rv.data
        assert b'catalog02' in rv.data

        rv = client.get('/catalog/catalog01')
        assert rv.status_code == 200
        assert 'Allow' in rv.headers
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'text/turtle'
        assert b'catalog01' in rv.data
        assert b'hasVersion "1.0"' in rv.data

        rv = client.put('/catalog/catalog01', data=datadir['catalog01_update.ttl'])
        # assert rv.status_code == 200
        # assert rv.json['message'] == 'Ok'
        print(rv.data)
        assert rv.json['message'] == 'Ok'

        rv = client.get('/catalog/catalog01')
        assert rv.status_code == 200
        assert b'catalog01' in rv.data
        assert b'hasVersion "2.0"' in rv.data

        rv = client.delete('/catalog/catalog01')
        assert rv.status_code == 204

        rv = client.get('/catalog/catalog01')
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.put('/catalog/catalog01', data=datadir['catalog01_update.ttl'])
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.delete('/catalog/catalog01')
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.get('/catalog')
        assert rv.status_code == 200
        assert b'catalog01' not in rv.data
        assert b'catalog02' in rv.data

        rv = client.delete('/catalog/catalog02')
        assert rv.status_code == 204

        rv = client.get('/catalog')
        assert rv.status_code == 204

    def test_catalog_invalid(self, client, datadir):
        """Test invalid metadata to catalog layer"""
        rv = client.post('/catalog', data=datadir['catalog01_invalid_missingRequired.ttl'])
        assert rv.status_code == 405
        assert 'Validation Report\nConforms: False\nResults (9)' in rv.json['message']

    def test_dataset(self, client, datadir):
        """Testing post, get, put and delete to dataset"""
        rv = client.post('/dataset', data=datadir['dataset01.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.post('/dataset', data=datadir['dataset02.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.get('/dataset')
        assert rv.status_code == 200
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'text/plain'
        assert b'breedb' in rv.data
        assert b'dataset02' in rv.data

        rv = client.get('/dataset/breedb', )
        assert rv.status_code == 200
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'text/turtle'
        assert b'breedb' in rv.data
        assert b'hasVersion "1.0"' in rv.data

        rv = client.put('/dataset/breedb', data=datadir['dataset01_update.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.get('/dataset/breedb', )
        assert rv.status_code == 200
        assert b'breedb' in rv.data
        assert b'hasVersion "2.0"' in rv.data

        rv = client.delete('/dataset/breedb')
        assert rv.status_code == 204

        rv = client.get('/dataset/breedb')
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.put('/dataset/breedb', data=datadir['dataset01_update.ttl'])
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.delete('/dataset/breedb')
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.get('/dataset')
        assert rv.status_code == 200
        assert b'breedb' not in rv.data
        assert b'dataset02' in rv.data

        rv = client.delete('/dataset/dataset02')
        assert rv.status_code == 204

        rv = client.get('/dataset')
        assert rv.status_code == 204

    def test_dataset_invalid(self, client, datadir):
        """Test invalid metadata to dataset layer"""
        rv = client.post('/dataset', data=datadir['dataset01_invalid_missingRequired.ttl'])
        assert rv.status_code == 405
        assert 'Validation Report\nConforms: False\nResults (9)' in rv.json['message']

    def test_distribution(self, client, datadir):
        """Testing post, get, put and delete to distribution"""

        rv = client.post('/distribution', data=datadir['dist01.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.post('/distribution', data=datadir['dist02.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.get('/distribution')
        assert rv.status_code == 200
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'text/plain'
        assert b'breedb-sparql' in rv.data
        assert b'dist02' in rv.data

        rv = client.get('/distribution/breedb-sparql')
        assert rv.status_code == 200
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'text/turtle'
        assert b'breedb-sparql' in rv.data
        assert b'hasVersion "1.0"' in rv.data

        rv = client.put('/distribution/breedb-sparql', data=datadir['dist01_update.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.get('/distribution/breedb-sparql')
        assert rv.status_code == 200
        assert b'breedb-sparql' in rv.data
        assert b'hasVersion "2.0"' in rv.data

        rv = client.delete('/distribution/breedb-sparql')
        assert rv.status_code == 204

        rv = client.get('/distribution/breedb-sparql')
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.put('/distribution/breedb-sparql', data=datadir['dist01_update.ttl'])
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.get('/distribution')
        assert rv.status_code == 200
        assert b'breedb-sparql' not in rv.data
        assert b'dist02' in rv.data

        rv = client.delete('/distribution/dist02')
        assert rv.status_code == 204

        rv = client.get('/distribution')
        assert rv.status_code == 204

    def test_distribution_invalid(self, client, datadir):
        """Test invalid metadata to distribution layer"""
        rv = client.post('/distribution', data=datadir['dist01_invalid_missingRequired.ttl'])
        assert rv.status_code == 405
        assert 'message' in rv.json
        assert 'Validation Report\nConforms: False\nResults (9)' in rv.json['message']

        rv = client.post('/distribution', data=datadir['dist01_invalid_2URLs.ttl'])
        assert rv.status_code == 405
        assert 'message' in rv.json
        assert 'Validation Report\nConforms: False\nResults (1)' in rv.json['message']


class TestMIMETypes:
    """Test different MIME types for GET and POST methods"""
    def test_fdp_n3(self, client_new_store, datadir):
        with open(datadir['fdp.n3'], 'rb') as f:
            data = f.read()

        rv = client_new_store.post('/fdp', data=datadir['fdp.n3'], content_type = 'text/n3')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client_new_store.get('/fdp', headers={'accept': 'text/n3'})
        assert rv.status_code == 200
        assert rv.mimetype == 'text/n3'
        b'<http://0.0.0.0/fdp> <http://rdf.biosemantics.org/ontologies/fdp-o#metadataIssued> "2019-04-09T10:01:00"^^<http://www.w3.org/2001/XMLSchema#dateTime> .' in rv.data
        # assert data == rv.data

    # hard to test fulltext due to the random orders of output terms, so test only one term
    def test_fdp_xml(self, client_new_store, datadir):
        rv = client_new_store.post('/fdp', data=datadir['fdp.rdf'], content_type = 'application/rdf+xml')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client_new_store.get('/fdp', headers={'accept': 'application/rdf+xml'})
        assert rv.status_code == 200
        assert rv.mimetype == 'application/rdf+xml'
        assert b'<fdp:metadataIssued rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2019-04-09T10:01:00</fdp:metadataIssued>' in rv.data

    def test_fdp_jsonld(self, client_new_store, datadir):
        rv = client_new_store.post('/fdp', data=datadir['fdp.jsonld'], content_type = 'application/ld+json')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client_new_store.get('/fdp', headers={'accept': 'application/ld+json'})
        assert rv.status_code == 200
        assert rv.mimetype == 'application/ld+json'
        rv.json[0]['http://rdf.biosemantics.org/ontologies/fdp-o#metadataIssued'] == {
            '@type': 'http://www.w3.org/2001/XMLSchema#dateTime', '@value': '2019-04-09T10:01:00'}

    def test_fdp_nt(self, client_new_store, datadir):
        rv = client_new_store.post('/fdp', data=datadir['fdp.nt'], content_type = 'application/n-triples')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client_new_store.get('/fdp', headers={'accept': 'application/n-triples'})
        assert rv.status_code == 200
        assert rv.mimetype == 'application/n-triples'
        b'<http://0.0.0.0/fdp> <http://rdf.biosemantics.org/ontologies/fdp-o#metadataIssued> "2019-04-09T10:01:00"^^<http://www.w3.org/2001/XMLSchema#dateTime> .' in rv.data