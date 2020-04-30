import pytest

from fdp.fdp import app, initGraph


def setup_module(module):
    '''Initialize in-memory graph with minimal data.'''
    initGraph(host='0.0.0.0', port=8080, dataFile=None, endpoint='http://0.0.0.0:8890/sparql')


@pytest.fixture
def client():
    '''Build http client'''
    with app.test_client() as client:
        yield client
    # Nothing to do, no connections to close.


# datadir fixture provided via pytest-datadir-ng
def test_fdp(client, datadir):
    """Testing post and get to fdp"""
    rv = client.post('/fdp', data=datadir['fdp_post.ttl'])
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


def test_catalog(client, datadir):
    """Testing post and get to catalog"""
    rv = client.post('/catalog/', data=datadir['catalog01_post.ttl'])
    assert rv.status_code == 200
    assert 'message' in rv.json
    assert rv.json['message'] == 'Ok'

    rv = client.post('/catalog/', data=datadir['catalog02_post.ttl'])
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


def test_dataset(client, datadir):
    """Testing post and get to dataset"""
    rv = client.post('/dataset/', data=datadir['dataset01_post.ttl'])
    assert rv.status_code == 200
    assert rv.json['message'] == 'Ok'

    rv = client.post('/dataset/', data=datadir['dataset02_post.ttl'])
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


def test_distribution(client, datadir):
    """Testing post and get to distribution"""

    rv = client.post('/distribution/', data=datadir['dist01_post.ttl'])
    assert rv.status_code == 200
    assert rv.json['message'] == 'Ok'

    rv = client.post('/distribution/', data=datadir['dist02_post.ttl'])
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
