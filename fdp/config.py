
from fdp.fairgraph import FAIRGraph

def build_base_uri(host, port):
    if not host.startswith('http'):
        host = f'http://{host}'
    if int(port) == 80:
        base_uri = host
    else:
        base_uri = f'{host}:{port}'
    return base_uri

_fairgraph = None

def init_fairgraph(host, port, endpoint):
    base_uri = build_base_uri(host, port)
    global _fairgraph
    _fairgraph = FAIRGraph(base_uri, endpoint)

def get_fairgraph():
    return _fairgraph
