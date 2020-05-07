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
    app.graph = g

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
    else:
        accept_header = 'text/turtle'

    serialized_graph = graph.serialize(uri, fmt)
    if serialized_graph is None:
        #TODO redesign the response body?
        resp = make_response({'message': 'Not Found'}, 404)
    else:
        resp = make_response(serialized_graph)
        resp.headers['Content-Type'] = accept_header
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
        return httpResponse(app.graph, app.graph.fdpURI())

    @api.expect(model)
    def post(self):
        '''
        Create new FDP metadata
        '''
        req_data = request.data
        req_data = req_data.decode('utf-8')
        valid, message = validator.validateFDP(req_data)
        # TODO validate to make sure there is only one subject
        if valid:
            app.graph.post(data=req_data, format='turtle')
            return make_response({'message': 'Ok'}, 200)
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
        return httpResponse(app.graph, app.graph.catURI(id))

    @api.expect(model)
    def post(self, id):
        '''
        POST catalog metadata
        '''
        req_data = request.data
        req_data = req_data.decode('utf-8')
        valid, message = validator.validateCatalog(req_data)
        # TODO validate to make sure there is only one subject
        if valid:
            app.graph.post(data=req_data, format='turtle')
            return make_response({'message': 'Ok'}, 200)
        else:
            return make_response({'message': message}, 500)

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
        return httpResponceNav(app.graph, 'Catalog')

    @api.expect(model)
    def post(self):
        '''
        POST catalog metadata
        '''
        req_data = request.data
        req_data = req_data.decode('utf-8')
        valid, message = validator.validateCatalog(req_data)
        if valid:
            app.graph.post(data=req_data, format='turtle')
            return make_response({'message': 'Ok'}, 200)
        else:
            return make_response({'message': message}, 500)

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
        return httpResponse(app.graph, app.graph.datURI(id))

    @api.expect(model)
    def post(self, id):
        '''
        POST dataset metadata
        '''
        req_data = request.data
        req_data = req_data.decode('utf-8')
        valid, message = validator.validateDataset(req_data)
        # TODO validate to make sure there is only one subject
        if valid:
            app.graph.post(data=req_data, format='turtle')
            return make_response({'message': 'Ok'}, 200)
        else:
            return make_response({'message': message}, 500)

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
        return httpResponceNav(app.graph, 'Dataset')

    @api.expect(model)
    def post(self):
        '''
        POST dataset metadata
        '''
        req_data = request.data
        req_data = req_data.decode('utf-8')
        valid, message = validator.validateDataset(req_data)
        if valid:
            app.graph.post(data=req_data, format='turtle')
            return make_response({'message': 'Ok'}, 200)
        else:
            return make_response({'message': message}, 500)

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
        return httpResponse(app.graph, app.graph.distURI(id))

    @api.expect(model)
    def post(self, id):
        '''
        POST distribution metadata
        '''
        req_data = request.data
        req_data = req_data.decode('utf-8')
        # TODO validate to make sure there is only one subject
        valid, message = validator.validateDistribution(req_data)
        if valid:
            app.graph.post(data=req_data, format='turtle')
            return make_response({'message': 'Ok'}, 200)
        else:
            return make_response({'message': message}, 500)

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
        return httpResponceNav(app.graph, 'Distribution')

    @api.expect(model)
    def post(self):
        '''
        POST distribution metadata
        '''
        req_data = request.data
        req_data = req_data.decode('utf-8')

        valid, message = validator.validateDistribution(req_data)
        if valid:
            app.graph.post(data=req_data, format='turtle')
            return make_response({'message': 'Ok'}, 200)
        else:
            return make_response({'message': message}, 500)

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


def run_app(host, port, dataFile, endpoint):
    initGraph(host=host, port=port, dataFile=dataFile, endpoint=endpoint)
    app.run(host=host, port=port, debug=True)