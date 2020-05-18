import pytest

from fdp.fdp import app, initGraph


@pytest.fixture
def client():
    '''Build http client'''
    with app.test_client() as client:
        yield client

class BaseEndpointTests:
    '''All implementations fo FDP should work for all endpoints.'''

    # datadir fixture provided via pytest-datadir-ng
    def test_fdp(self, client, datadir):
        """Testing post and get to fdp"""
        rv = client.post('/fdp', data=datadir['fdp.ttl'])
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client.post('/fdp', data=datadir['fdp_invalid_missingRequired.ttl'])
        assert rv.status_code == 500
        assert 'message' in rv.json
        assert 'Validation Report\nConforms: False\nResults (8)' in rv.json['message']

        rv = client.post('/fdp', data=datadir['fdp_invalid_unknownTerms.ttl'])
        assert rv.status_code == 500
        assert 'message' in rv.json
        print(rv.json['message'])
        assert 'Validation Report\nConforms: False\nResults (2)' in rv.json['message']

        rv = client.post('/fdp', data=datadir['fdp_invalid_blank.ttl'])
        assert rv.status_code == 500
        assert 'message' in rv.json
        assert 'Empty content in metadtata' in rv.json['message']

        rv = client.post('/fdp', data=datadir['fdp_invalid_2foucsNodes.ttl'])
        assert rv.status_code == 500
        assert 'message' in rv.json
        assert 'FDP layer allows only one subject in metadata' in rv.json['message']

        rv = client.get('/fdp')
        assert rv.status_code == 200
        assert 'Allow' in rv.headers
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'text/turtle'
        assert b'hasVersion "0.1"' in rv.data
        assert b'metadataIssued "2019-04-09T10:01:00"^^xsd:dateTime' in rv.data

        rv = client.delete('/fdp')
        assert rv.status_code == 405
        assert 'message' in rv.json
        assert rv.json['message'] == 'Method Not Allowed'


    def test_catalog(self, client, datadir):
        """Testing post and get to catalog"""
        rv = client.post('/catalog/', data=datadir['catalog01.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.post('/catalog/', data=datadir['catalog01_invalid_missingRequired.ttl'])
        assert rv.status_code == 500
        assert 'Validation Report\nConforms: False\nResults (9)' in rv.json['message']

        rv = client.post('/catalog/', data=datadir['catalog02.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.get('/catalog/')
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

        rv = client.get('/catalog/catalog02',
                        headers = {'Accept': 'application/ld+json'})
        assert rv.status_code == 200
        assert 'Allow' in rv.headers
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'application/ld+json'
        assert b'catalog02' in rv.data

        rv = client.delete('/catalog/catalog01')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client.get('/catalog/catalog01')
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.delete('/catalog/catalog01')
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.get('/catalog/')
        assert rv.status_code == 200
        assert b'catalog01' not in rv.data
        assert b'catalog02' in rv.data

        rv = client.delete('/catalog/catalog02')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client.get('/catalog/')
        assert rv.status_code == 204


    def test_dataset(self, client, datadir):
        """Testing post and get to dataset"""
        rv = client.post('/dataset/', data=datadir['dataset01.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.post('/dataset/', data=datadir['dataset01_invalid_missingRequired.ttl'])
        assert rv.status_code == 500
        assert 'Validation Report\nConforms: False\nResults (9)' in rv.json['message']

        rv = client.post('/dataset/', data=datadir['dataset02.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.get('/dataset/')
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

        rv = client.get('/dataset/dataset02',
                        headers = {'Accept': 'application/ld+json'})
        assert rv.status_code == 200
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'application/ld+json'
        assert b'dataset02' in rv.data

        rv = client.delete('/dataset/breedb')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client.get('/dataset/breedb')
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.delete('/dataset/breedb')
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.get('/dataset/')
        assert rv.status_code == 200
        assert b'breedb' not in rv.data
        assert b'dataset02' in rv.data

        rv = client.delete('/dataset/dataset02')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client.get('/dataset/')
        assert rv.status_code == 204


    def test_distribution(self, client, datadir):
        """Testing post and get to distribution"""

        rv = client.post('/distribution/', data=datadir['dist01.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.post('/distribution/', data=datadir['dist01_invalid_missingRequired.ttl'])
        assert rv.status_code == 500
        assert 'message' in rv.json
        assert 'Validation Report\nConforms: False\nResults (9)' in rv.json['message']

        rv = client.post('/distribution/', data=datadir['dist01_invalid_2URLs.ttl'])
        assert rv.status_code == 500
        assert 'message' in rv.json
        assert 'Validation Report\nConforms: False\nResults (1)' in rv.json['message']

        rv = client.post('/distribution/', data=datadir['dist02.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.get('/distribution/')
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

        rv = client.get('/distribution/dist02',
                        headers = {'Accept': 'application/ld+json'})
        assert rv.status_code == 200
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'application/ld+json'
        assert b'dist02' in rv.data

        rv = client.delete('/distribution/breedb-sparql')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client.get('/distribution/breedb-sparql')
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.get('/distribution/')
        assert rv.status_code == 200
        assert b'breedb-sparql' not in rv.data
        assert b'dist02' in rv.data

        rv = client.delete('/distribution/dist02')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client.get('/distribution/')
        assert rv.status_code == 204



class TestFairgraphEndpoints(BaseEndpointTests):
    '''Test endpoints the in-memory graph implementation'''
    def setup_class(self):
        # initGraph(host='0.0.0.0', port=8080, dataFile='./samples/minimal.ttl', endpoint=None)
        initGraph(host='0.0.0.0', port=8080)

class TestStoregraphEndpoints(BaseEndpointTests):
    '''Test endpoints using the SPARQL graph implementation'''
    def setup_class(self):
        # initGraph(host='0.0.0.0', port=8080, dataFile=None, endpoint='http://0.0.0.0:8890/sparql')
        initGraph(host='0.0.0.0', port=8080, endpoint='http://0.0.0.0:8890/sparql')