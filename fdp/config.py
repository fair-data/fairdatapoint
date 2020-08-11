
from fdp.fairgraph import FAIRGraph

def build_base_uri(host, port):
    if host == 'localhost':
        host = 'http://127.0.0.1'
    elif not host.startswith('http'):
        host = f'http://{host}'
    if int(port) == 80:
        base_uri = host
    else:
        base_uri = f'{host}:{port}'
    return base_uri

_fairgraph = None
_grlc_endpoint = None
_sparql_endpoint = None

def init_fairgraph(host, port, sparql_endpoint):
    base_uri = build_base_uri(host, port)
    global _fairgraph
    _fairgraph = FAIRGraph(base_uri, sparql_endpoint)

def get_fairgraph():
    return _fairgraph

def init_grlc(grlc_endpoint, sparql_endpoint):
    global _grlc_endpoint
    _grlc_endpoint = grlc_endpoint + '/api-local'
    global _sparql_endpoint
    _sparql_endpoint = sparql_endpoint

def get_grlc_endpoint():
    return _grlc_endpoint

def get_sparql_endpoint():
    return _sparql_endpoint
