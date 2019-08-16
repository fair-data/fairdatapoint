# -*- coding: utf-8 -*-

from bottle import get, run, static_file, redirect, response, request,  \
    install
from datetime import datetime
from functools import wraps
from logging import getLogger, INFO, StreamHandler

from .utils import FDPath
from .metadata import FAIRGraph as ConfigFAIRGraph
from .fairgraph import FAIRGraph as RDFFAIRGraph

def logHttpRequests(fn):
    """Log HTTP requests into log file using Common Log Format"""
    logger = getLogger(__name__)
    logger.setLevel(INFO)
    logger.addHandler(StreamHandler())

    @wraps(fn)
    def _log_to_logger(*args, **kwargs):
        request_time = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        logger.info('%s - - [%s] "%s %s %s" %d' % (
            request.remote_addr,
            request_time,
            request.method,
            request.urlparts.path,
            request.get('SERVER_PROTOCOL'),
            response.status_code))
        return fn(*args, **kwargs)
    return _log_to_logger

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

    if serialized_graph is None:
        response.status = 404  # web resource not found
        return

    response.content_type = 'text/plain'
    response.set_header('Allow', 'GET')

    return serialized_graph


# HTTP request handlers
@get(['/', '/doc', '/doc/'])
def defaultPage():
    redirect('/doc/index.html')


@get(FDPath('doc', '<fname:path>'))
def sourceDocFiles(fname):
    return static_file(fname, root='doc')


@get(FDPath('fdp'))
def getFdpMetadata():
    graph = data['graph']
    return httpResponse(graph, graph.fdpURI())


@get(FDPath('cat', '<catalog_id>'))
def getCatalogMetadata(catalog_id):
    graph = data['graph']
    return httpResponse(graph, graph.catURI(catalog_id))


@get(FDPath('dat', '<dataset_id>'))
def getDatasetMetadata(dataset_id):
    graph = data['graph']
    return httpResponse(graph, graph.datURI(dataset_id))


@get(FDPath('dist', '<distribution_id>'))
def getDistributionMetadata(distribution_id):
    graph = data['graph']
    return httpResponse(graph, graph.distURI(distribution_id))

def run_app(host, port, dataFile):
    # log HTTP requests
    install(logHttpRequests)
    initGraph(host=host, port=port, dataFile=dataFile)
    run(host=host, port=port)
