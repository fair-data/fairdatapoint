# -*- coding: utf-8 -*-

from flask import Flask, make_response, request, redirect, send_from_directory
from flask_restplus import Api, Resource, Namespace

from .utils import FDPath
from .metadata import FAIRGraph as ConfigFAIRGraph
from .fairgraph import FAIRGraph as RDFFAIRGraph
from .storegraph import StoreFAIRGraph
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

# Data structure for holding data used
data = {}

def initGraph(host, port, dataFile, endpoint):
    scheme = 'http'
    host = '{}:{}'.format(host, port) # TODO: fix for port 80
    base_uri = '{}://{}'.format(scheme, host)

    if dataFile and dataFile.endswith('.ini'):
        # populate FAIR metadata from config file
        g = ConfigFAIRGraph(base_uri, dataFile)
    elif dataFile and dataFile.endswith('.ttl'):
        # populate FAIR metadata from turtle file
        g = RDFFAIRGraph(base_uri, dataFile)
    elif endpoint:
        print('Using store graph')
        g = StoreFAIRGraph(base_uri, endpoint)
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
    if serialized_graph is None:
        resp = make_response({'message': 'Not Found'}, 404)
    else:
        resp = make_response(serialized_graph)
        resp.headers['Content-Type'] = 'text/plain'
        resp.headers['Allow'] = 'GET'

    return resp

def httpResponceNav(graph, layer):
    """HTTP response: metadata navigations"""

    s = graph.navURI(layer)

    if s:
        resp = make_response('\n'.join(s), 200)
    else:
        resp = make_response({'message': 'No Content'}, 204)

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

@ns.route('fdp')
class FDPResource(Resource):
    model = api.parser()
    model.add_argument('text', type=str, location='json')

    def get(self):
        '''
        FDP metadata
        '''
        graph = data['graph']
        return httpResponse(graph, graph.fdpURI())

    @api.expect(model)
    def post(self):
        '''
        Create new FDP metadata
        '''
        req_data = request.data
        req_data = req_data.decode('utf-8')
        valid, message = validator.validateFDP(req_data)
        # TODO validate to make sure there is only one subject
        graph = data['graph']
        if valid:
            graph.post(data=req_data, format='turtle')
            return make_response({'message': 'OK'}, 200)
        else:
            return make_response({'message': message}, 500)

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
        graph = data['graph']
        return httpResponse(graph, graph.catURI(id))

    @api.expect(model)
    def post(self, id):
        '''
        POST catalog metadata
        '''
        req_data = request.data
        req_data = req_data.decode('utf-8')
        valid, message = validator.validateCatalog(req_data)
        # TODO validate to make sure there is only one subject
        graph = data['graph']
        if valid:
            graph.post(data=req_data, format='turtle')
            return make_response({'message': 'OK'}, 200)
        else:
            return make_response({'message': message}, 500)

    def delete(self, id):
        '''
        Delete the catalog ID and metadata
        '''
        graph = data['graph']
        if not graph.URIexists(graph.catURI(id)):
            return make_response({'message': 'Not Found'}, 404)
        graph.deleteURI(graph.catURI(id))
        return make_response({'message': 'OK'}, 200)

@ns.route('catalog/')
class CatalogPostResource(Resource):
    model = api.parser()
    model.add_argument('text', type=str, location='json')

    def get(self):
        '''
        Get the list of catalog URIs
        '''
        graph = data['graph']
        return httpResponceNav(graph, 'Catalog')

    @api.expect(model)
    def post(self):
        '''
        POST catalog metadata
        '''
        req_data = request.data
        req_data = req_data.decode('utf-8')
        valid, message = validator.validateCatalog(req_data)
        graph = data['graph']
        if valid:
            data['graph'].post(data=req_data, format='turtle')
            return make_response({'message': 'Ok'}, 200)
        else:
            return make_response({'message': message}, 500)

    def delete(self):
        """Delete all catalog metadata"""
        graph = data['graph']
        graph.deleteURILayer('Catalog')
        return make_response({'message': 'OK'}, 200)

@ns.route('dataset/<id>')
class DatasetMetadataGetterResource(Resource):
    model = api.parser()
    model.add_argument('text', type=str, location='json')
    def get(self, id):
        '''
        Dataset metadata
        '''
        graph = data['graph']
        return httpResponse(graph, graph.datURI(id))

    @api.expect(model)
    def post(self, id):
        '''
        POST dataset metadata
        '''
        req_data = request.data
        req_data = req_data.decode('utf-8')
        valid, message = validator.validateDataset(req_data)
        # TODO validate to make sure there is only one subject
        graph = data['graph']
        if valid:
            graph.post(data=req_data, format='turtle')
            return make_response({'message': 'OK'}, 200)
        else:
            return make_response({'message': message}, 500)

    def delete(self, id):
        '''
        Delete the dataset ID and metadata
        '''
        graph = data['graph']
        if not graph.URIexists(graph.datURI(id)):
            return make_response({'message': 'Not Found'}, 404)
        graph.deleteURI(graph.datURI(id))
        return make_response({'message': 'OK'}, 200)

@ns.route('dataset/')
class DatasetMetadataPostResource(Resource):
    model = api.parser()
    model.add_argument('text', type=str, location='json')

    def get(self):
        '''
        Get the list of dataset URIs
        '''
        graph = data['graph']
        return httpResponceNav(graph, 'Dataset')

    @api.expect(model)
    def post(self):
        '''
        POST dataset metadata
        '''
        req_data = request.data
        req_data = req_data.decode('utf-8')
        valid, message = validator.validateDataset(req_data)
        if valid:
            data['graph'].post(data=req_data, format='turtle')
            return make_response({'message': 'Ok'}, 200)
        else:
            return make_response({'message': message}, 500)

    def delete(self):
        """Delete all dataset metadata"""
        graph = data['graph']
        graph.deleteURILayer('Dataset')
        return make_response({'message': 'OK'}, 200)

@ns.route('distribution/<id>')
class DistributionGetterResource(Resource):
    model = api.parser()
    model.add_argument('text', type=str, location='json')
    def get(self, id):
        '''
        Dataset distribution metadata
        '''
        graph = data['graph']
        return httpResponse(graph, graph.distURI(id))

    @api.expect(model)
    def post(self, id):
        '''
        POST distribution metadata
        '''
        req_data = request.data
        req_data = req_data.decode('utf-8')
        # TODO validate to make sure there is only one subject
        valid, message = validator.validateDistribution(req_data)
        graph = data['graph']
        if valid:
            graph.post(data=req_data, format='turtle')
            return make_response({'message': 'OK'}, 200)
        else:
            return make_response({'message': message}, 500)

    def delete(self, id):
        '''
        Delete the distribution ID and metadata
        '''
        graph = data['graph']
        if not graph.URIexists(graph.distURI(id)):
            return make_response({'message': 'Not Found'}, 404)
        graph.deleteURI(graph.distURI(id))
        return make_response({'message': 'OK'}, 200)

@ns.route('distribution/')
class DistributionPostResource(Resource):
    model = api.parser()
    model.add_argument('text', type=str, location='json')

    def get(self):
        '''
        Get the list of distribution URIs
        '''
        graph = data['graph']
        return httpResponceNav(graph, 'Distribution')

    @api.expect(model)
    def post(self):
        '''
        POST distribution metadata
        '''
        req_data = request.data
        req_data = req_data.decode('utf-8')

        valid, message = validator.validateDistribution(req_data)
        if valid:
            data['graph'].post(data=req_data, format='turtle')
            return make_response({'message': 'Ok'}, 200)
        else:
            return make_response({'message': message}, 500)

    def delete(self):
        """Delete all distribution metadata"""
        graph = data['graph']
        graph.deleteURILayer('Distribution')
        return make_response({'message': 'OK'}, 200)

@ns.route('dump/')
class DumpResource(Resource):
    def get(self):
        '''
        Dataset distribution metadata
        '''
        graph = data['graph']
        serialized_graph = graph._graph.serialize(format='turtle').decode('utf-8')
        resp = make_response(serialized_graph)

        resp.headers['Content-Type'] = 'text/plain'
        resp.headers['Allow'] = 'GET'
        return resp


def run_app(host, port, dataFile, endpoint):
    initGraph(host=host, port=port, dataFile=dataFile, endpoint=endpoint)
    app.run(host=host, port=port, debug=True)
