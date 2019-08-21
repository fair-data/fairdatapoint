# -*- coding: utf-8 -*-

#from bottle import get, run, static_file, redirect, response, request,  \
#    install
from flask import Flask, make_response, request, redirect, send_from_directory

app = Flask(__name__)

from .utils import FDPath
from .metadata import FAIRGraph as ConfigFAIRGraph
from .fairgraph import FAIRGraph as RDFFAIRGraph

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


@app.route(FDPath('fdp'), methods=['GET'])
def getFdpMetadata():
    graph = data['graph']
    return httpResponse(graph, graph.fdpURI())


@app.route(FDPath('cat', '<catalog_id>'), methods=['GET'])
def getCatalogMetadata(catalog_id):
    graph = data['graph']
    return httpResponse(graph, graph.catURI(catalog_id))


@app.route(FDPath('dat', '<dataset_id>'), methods=['GET'])
def getDatasetMetadata(dataset_id):
    graph = data['graph']
    return httpResponse(graph, graph.datURI(dataset_id))


@app.route(FDPath('dist', '<distribution_id>'), methods=['GET'])
def getDistributionMetadata(distribution_id):
    graph = data['graph']
    return httpResponse(graph, graph.distURI(distribution_id))

def run_app(host, port, dataFile):
    initGraph(host=host, port=port, dataFile=dataFile)
    app.run(host=host, port=port)
