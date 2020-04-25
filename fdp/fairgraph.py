from rdflib import ConjunctiveGraph, Graph
from rdflib.term import URIRef

API_ENDPOINTS = {'/fdp', '/doc', '/catalog', '/dataset', '/distribution'}

class FAIRGraph(object):
    def __init__(self, base_uri, ttl_file):
        # UPGRADE: use rdflib.plugins.stores.sparqlstore.SPARQLStore
        # for SPARQL backend.
        self._graph = ConjunctiveGraph()
        self._graph.parse(ttl_file, format="n3")
        self._base_uri = base_uri

    def _buildURI(self, endpoint, id=None):
        assert (endpoint in API_ENDPOINTS), 'Invalid endpoint'
        id = '' if id is None else '/%s' % str(id)
        return self._base_uri + endpoint + id

    def fdpURI(self):
        return self._buildURI('/fdp')

    def catURI(self, id):
        return self._buildURI('/catalog', id)

    def addCatURI(self, data, format):
        self._graph.parse(data=data, format=format)

    def datURI(self, id):
        return self._buildURI('/dataset', id)

    def distURI(self, id):
        return self._buildURI('/distribution', id)

    def serialize(self, uri, mime_type):
        g = Graph()
        # Copy namespaces from base graph
        for prefix,ns_uri in self._graph.namespaces():
            g.bind(prefix, ns_uri)

        # Search for triples which match the given subject
        matchPattern = (URIRef(uri), None, None)
        g += self._graph.triples( matchPattern )

        if len(g.all_nodes()) > 0:
            return g.serialize(format='turtle').decode('utf-8')
        else:
            return None # 404 !
