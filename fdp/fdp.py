# -*- coding: utf-8 -*-

from flask import Flask, make_response, request, redirect, send_from_directory
from flask_restplus import Api, Resource, Namespace, fields

from .utils import FDPath
from .metadata import FAIRGraph as ConfigFAIRGraph
from .fairgraph import FAIRGraph as RDFFAIRGraph
from .__init__ import __version__ as version

app = Flask(__name__)
api = Api(app, version=version, title='FAIR Data Point API',
    description='FAIR Data Point allows data owners to expose datasets in a FAIR ' \
                'manner and data users to discover properties about offered datasets.',
)

ns = Namespace('metadata-controller', description='FDP metadata')
api.add_namespace(ns, path='/')


# Data structure for holding data used
data = {}

def initGraph(host, port, dataFile):
    scheme = 'http'
    host = '{}:{}'.format(host, port) # TODO: fix for port 80
    base_uri = '{}://{}'.format(scheme, host)

    if dataFile.endswith('.ini'):
        # populate FAIR metadata from config file
        g = ConfigFAIRGraph(base_uri, dataFile)
    elif dataFile.endswith('.ttl'):
        # populate FAIR metadata from turtle file
        g = RDFFAIRGraph(base_uri, dataFile)
    else:
        raise Exception('Unknown data format')
    data['graph'] = g

def httpResponse(graph, uri):
    """HTTP response: FAIR metadata in RDF and JSON-LD formats"""
    accept_header = request.headers.get('Accept')
    fmt = 'turtle'  # default RDF serialization
    mime_types = {
        'text/turtle': 'turtle',
        'application/rdf+xml': 'xml',
        'application/ld+json': 'json-ld',
        'application/n-triples': 'nt'
    }

    if accept_header in mime_types:
        fmt = mime_types[accept_header]

    serialized_graph = graph.serialize(uri, fmt)
    resp = make_response(serialized_graph)

    if serialized_graph is None:
        return 'Web resource not found', 404

    resp.headers['Content-Type'] = 'text/plain'
    resp.headers['Allow'] = 'GET'
    return resp


# HTTP request handlers
@app.route('/')
@app.route('/doc/')
def defaultPage():
    return redirect('/doc/index.html')


@app.route(FDPath('doc', '<path:fname>'))
def sourceDocFiles(fname):
    return send_from_directory('doc', fname)

@ns.route('fdp/')
class FDPResource(Resource):
    def get(self):
        '''
        FDP metadata
        '''
        graph = data['graph']
        return httpResponse(graph, graph.fdpURI())

    def patch(self):
        '''
        Update fdp metadata
        '''
        return '', 500

@ns.route('catalog/<id>')
class CatalogGetterResource(Resource):
    def get(self, id):
        '''
        Catalog metadata
        '''
        graph = data['graph']
        return httpResponse(graph, graph.catURI(id))

@ns.route('catalog/')
class CatalogPostResource(Resource):
    model = api.parser()
    model.add_argument('text', type=str, location='json')

    @api.expect(model)
    def post(self):
        '''
        POST catalog metadata
        '''
        return '', 500

@ns.route('dataset/<id>')
class DatasetMetadataGetterResource(Resource):
    def get(self, id):
        '''
        Dataset metadata
        '''
        graph = data['graph']
        return httpResponse(graph, graph.datURI(id))


@ns.route('dataset/')
class DatasetMetadataPostResource(Resource):
    def post(self):
        '''
        POST dataset metadata
        '''
        return '', 500


@ns.route('distribution/<id>')
class DistributionGetterResource(Resource):
    def get(self, id):
        '''
        Dataset distribution metadata
        '''
        graph = data['graph']
        return httpResponse(graph, graph.distURI(id))

@ns.route('distribution/')
class DistributionPostResource(Resource):
    def post(self):
        '''
        POST distribution metadata
        '''
        return '', 500


def run_app(host, port, dataFile):
    initGraph(host=host, port=port, dataFile=dataFile)
    app.run(host=host, port=port, debug=True)
