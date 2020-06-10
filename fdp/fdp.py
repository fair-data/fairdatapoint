# -*- coding: utf-8 -*-

from flask import Flask, make_response, request, redirect, send_from_directory
from flask_restplus import Api, Resource, Namespace

from .utils import FDPath
from .fairgraph import FAIRGraph
from .validator import FDPValidator
from .__init__ import __version__ as version

app = Flask(__name__)
api = Api(app, version=version, title='FAIR Data Point API',
    description='FAIR Data Point allows data owners to expose datasets in a FAIR ' \
                'manner and data users to discover properties about offered datasets.',
)

ns = Namespace('metadata-controller', description='FDP metadata')
api.add_namespace(ns, path='/')

validator = FDPValidator()

# TODO named graphs: application/trig, application/n-quads
MIME_TYPES = {
    'text/n3': 'n3',
    'text/turtle': 'turtle',
    'application/rdf+xml': 'xml',
    'application/ld+json': 'json-ld',
    'application/n-triples': 'nt',
}

def initGraph(host, port, endpoint=None):
    if host == 'localhost':
        host = 'http://127.0.0.1'
    elif not host.startswith('http'):
        host = f'http://{host}'
    if int(port) == 80:
        base_uri = host
    else:
        base_uri = f'{host}:{port}'
    if endpoint is None:
        g = FAIRGraph(base_uri)
    else:
        g = FAIRGraph(base_uri, endpoint)
    app.graph = g

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
    serialized_graph = app.graph.serialize(uri, fmt)
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

    s = app.graph.navURI(layer)
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
        app.graph.post(data=req_data, format=fmt)
        return make_response({'message': 'Ok'}, 200)
    else:
        return make_response({'message': message}, 500)


# HTTP request handlers
@app.route('/')
@app.route('/doc/')
def defaultPage():
    return redirect('/doc/index.html')


@app.route(FDPath('doc', '<path:fname>'))
def sourceDocFiles(fname):
    return send_from_directory('doc', fname)

@ns.route('fdp')
class FDPResource(Resource):
    model = api.parser()
    model.add_argument('text', type=str, location='json')

    def get(self):
        '''
        FDP metadata
        '''
        return httpResponse(app.graph.fdpURI())

    @api.expect(model)
    def post(self):
        '''
        Create new FDP metadata
        '''
        return httpResponsePost('FDP')

    def delete(self):
        '''
        Delete FDP metadata
        '''
        return make_response({'message': 'Method Not Allowed'}, 405)

@ns.route('catalog/<id>')
class CatalogGetterResource(Resource):
    model = api.parser()
    model.add_argument('text', type=str, location='json')

    def get(self, id):
        '''
        Catalog metadata
        '''
        return httpResponse(app.graph.catURI(id))

    def delete(self, id):
        '''
        Delete the catalog ID and metadata
        '''
        if not app.graph.URIexists(app.graph.catURI(id)):
            return make_response({'message': 'Not Found'}, 404)
        app.graph.deleteURI(app.graph.catURI(id))
        return make_response({'message': 'Ok'}, 200)

@ns.route('catalog/')
class CatalogPostResource(Resource):
    model = api.parser()
    model.add_argument('text', type=str, location='json')

    def get(self):
        '''
        Get the list of catalog URIs
        '''
        return httpResponseNav('Catalog')

    @api.expect(model)
    def post(self):
        '''
        POST catalog metadata
        '''
        return httpResponsePost('Catalog')

    def delete(self):
        """Delete all catalog metadata"""
        app.graph.deleteURILayer('Catalog')
        return make_response({'message': 'Ok'}, 200)

@ns.route('dataset/<id>')
class DatasetMetadataGetterResource(Resource):
    model = api.parser()
    model.add_argument('text', type=str, location='json')
    def get(self, id):
        '''
        Dataset metadata
        '''
        return httpResponse(app.graph.datURI(id))

    def delete(self, id):
        '''
        Delete the dataset ID and metadata
        '''
        if not app.graph.URIexists(app.graph.datURI(id)):
            return make_response({'message': 'Not Found'}, 404)
        app.graph.deleteURI(app.graph.datURI(id))
        return make_response({'message': 'Ok'}, 200)

@ns.route('dataset/')
class DatasetMetadataPostResource(Resource):
    model = api.parser()
    model.add_argument('text', type=str, location='json')

    def get(self):
        '''
        Get the list of dataset URIs
        '''
        return httpResponseNav('Dataset')

    @api.expect(model)
    def post(self):
        '''
        POST dataset metadata
        '''
        return httpResponsePost('Dataset')

    def delete(self):
        """Delete all dataset metadata"""
        app.graph.deleteURILayer('Dataset')
        return make_response({'message': 'Ok'}, 200)

@ns.route('distribution/<id>')
class DistributionGetterResource(Resource):
    model = api.parser()
    model.add_argument('text', type=str, location='json')
    def get(self, id):
        '''
        Dataset distribution metadata
        '''
        return httpResponse(app.graph.distURI(id))

    def delete(self, id):
        '''
        Delete the distribution ID and metadata
        '''
        if not app.graph.URIexists(app.graph.distURI(id)):
            return make_response({'message': 'Not Found'}, 404)
        app.graph.deleteURI(app.graph.distURI(id))
        return make_response({'message': 'Ok'}, 200)

@ns.route('distribution/')
class DistributionPostResource(Resource):
    model = api.parser()
    model.add_argument('text', type=str, location='json')

    def get(self):
        '''
        Get the list of distribution URIs
        '''
        return httpResponseNav('Distribution')

    @api.expect(model)
    def post(self):
        '''
        POST distribution metadata
        '''
        return httpResponsePost('Distribution')

    def delete(self):
        """Delete all distribution metadata"""
        app.graph.deleteURILayer('Distribution')
        return make_response({'message': 'Ok'}, 200)

@ns.route('dump/')
class DumpResource(Resource):
    def get(self):
        '''
        Dataset distribution metadata
        '''
        serialized_graph = app.graph.serialize(format='turtle').decode('utf-8')
        resp = make_response(serialized_graph)

        resp.headers['Content-Type'] = 'text/plain'
        resp.headers['Allow'] = 'GET'
        return resp

def init_app(host, port, endpoint):
    initGraph(host=host, port=port, endpoint=endpoint)
    return app