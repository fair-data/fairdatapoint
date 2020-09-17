from flask import make_response, request
from fdp.validator import FDPValidator
from fdp.config import get_fairgraph

validator = FDPValidator()
fairgraph = get_fairgraph()

# TODO named graphs: application/trig, application/n-quads
MIME_TYPES = {
    'text/n3': 'n3',
    'text/turtle': 'turtle',
    'application/rdf+xml': 'xml',
    'application/ld+json': 'json-ld',
    'application/n-triples': 'nt',
}

def httpResponse(uri):
    """HTTP response to a GET request for FAIR metadata.

    Args:
        uri (str): URI for target graph subject

    Returns:
        HTTP response: response to a GET request
    """
    accept_headers = request.headers.getlist('Accept')
    accept_headers = list(filter(lambda x: x in MIME_TYPES, accept_headers))
    if accept_headers:
        accept_header = accept_headers[0]
    else:
        accept_header = 'text/turtle' # default RDF serialization

    fmt = MIME_TYPES[accept_header]
    serialized_graph = fairgraph.serialize(uri, fmt)
    if serialized_graph is None:
        #TODO redesign the response body?
        resp = make_response({'message': 'Not Found'}, 404)
    else:
        resp = make_response(serialized_graph)
        resp.headers['Content-Type'] = accept_header
        resp.headers['Allow'] = 'GET'

    return resp

def httpResponseNav(layer):
    """HTTP responce to a GET request for metadata navagation.

    Args:
        layer(str): "FDP", "Catalog", "Dataset" or "Distribution"

    Returns:
        HTTP response: Responce to GET request for metadata navagation.
    """

    s = fairgraph.navURI(layer)
    if s:
        resp = make_response('\n'.join(s), 200)
    else:
        resp = make_response('', 204)

    resp.headers['Content-Type'] = 'text/plain'
    resp.headers['Allow'] = 'GET'
    return resp

def httpResponsePost(layer):
    """HTTP responce to a POST request.

    Args:
        layer(str): "FDP", "Catalog", "Dataset" or "Distribution".

    Returns:
        HTTP responce: Responce to POST request.
    """
    # common default content types from curl, urllib, requests and flask.client
    default_types = ['', None, 'multipart/form-data', 'application/x-www-form-urlencoded']
    mimetype = request.mimetype
    if mimetype in default_types:
        mimetype = 'text/turtle'
    elif mimetype not in MIME_TYPES:
        return make_response({'message': 'Unsupported Media Type'}, 415)
    fmt = MIME_TYPES[mimetype]

    req_data = request.data
    req_data = req_data.decode('utf-8')
    valid, message = validator.validate(req_data, fmt, layer)
    if valid:
        fairgraph.post(data=req_data, format=fmt)
        return make_response({'message': 'Ok'}, 200)
    else:
        return make_response({'message': message}, 405)

class FDP():
    def post():
        '''
        Create new FDP metadata
        '''
        return httpResponsePost('FDP')

    def get():
        '''
        Get FDP metadata
        '''
        return httpResponse(fairgraph.buildURI('FDP'))

    def put():
        '''
        Update FDP metadata
        '''
        targetURI = fairgraph.buildURI('FDP')
        if not fairgraph.URIexists(targetURI):
            return make_response({'message': 'Not Found'}, 404)
        fairgraph.deleteURI(targetURI)
        return httpResponsePost('FDP')

class Metadata():

    def __init__(self, layer):
        self.layer = layer

    def get_all(self):
        '''
        Get the list of catalog URIs
        '''
        return httpResponseNav(self.layer)

    def post(self):
        '''
        POST catalog metadata
        '''
        return httpResponsePost(self.layer)

    def get(self, id):
        '''
        Get Catalog metadata
        '''
        return httpResponse(fairgraph.buildURI(self.layer, id))

    def put(self, id):
        '''
        Update Catalog metadata
        '''
        targetURI = fairgraph.buildURI(self.layer, id)
        if not fairgraph.URIexists(targetURI):
            return make_response({'message': 'Not Found'}, 404)
        fairgraph.deleteURI(targetURI)
        #TODO validate the id of the request body
        return httpResponsePost(self.layer)

    def delete(self, id):
        '''
        Delete the catalog ID and metadata
        '''
        targetURI = fairgraph.buildURI(self.layer, id)
        if not fairgraph.URIexists(targetURI):
            return make_response({'message': 'Not Found'}, 404)
        fairgraph.deleteURI(targetURI)
        return make_response('', 204)

Catalog = Metadata('Catalog')
Dataset = Metadata('Dataset')
Distribution = Metadata('Distribution')