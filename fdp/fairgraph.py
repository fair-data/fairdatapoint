from rdflib import Graph, Namespace, URIRef
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore

API_ENDPOINTS = {'fdp', 'doc', 'catalog', 'dataset', 'distribution'}
DCAT = Namespace("http://www.w3.org/ns/dcat#")

class FAIRGraph(object):
    def __init__(self, base_uri, endpoint=None):
        self._base_uri = base_uri
        if endpoint is None:
            self._graph = Graph()     # memory store
        else:
            default_graph = URIRef(base_uri)
            store = SPARQLUpdateStore(endpoint)
            self._graph = Graph(store, identifier=default_graph)

    def buildURI(self, endpoint, id=None):
        endpoint = endpoint.lower()
        assert (endpoint in API_ENDPOINTS), 'Invalid endpoint'
        if id is None:
            uri = self._base_uri + '/' + endpoint
        else:
            uri = self._base_uri + '/' + endpoint + '/' + str(id)
        return uri

    def serialize(self, uri, format):
        g = self.matchURI(uri)
        if len(g.all_nodes()) > 0:
            return g.serialize(format=format)
        else:
            return None  # 404 !

    def URIexists(self, uri):
        return (URIRef(uri), None, None) in self._graph

    def matchURI(self, uri):
        g = Graph()
        # Copy namespaces from base graph
        for prefix, ns_uri in self._graph.namespaces():
            g.bind(prefix, ns_uri)
        # Search for triples which match the given subject
        matchPattern = (URIRef(uri), None, None)
        g += self._graph.triples(matchPattern)
        return g

    def post(self, data, format):
        """Overwrite all existing triples of a specific subject.
        """
        # Load data on the graph
        g = Graph()
        g.parse(data=data, format=format)
        # Remove all triples of specific subjects
        s_set = set(g.subjects())
        if s_set:
            for s in s_set:
                self._graph.remove((s, None, None))
            # if prefix conflicts with differnt ns_uris, it'll be suffixed with a number
            for prefix, ns_uri in g.namespaces():
                self._graph.bind(prefix, ns_uri)
            self._graph += g
            self._graph.commit()

    def deleteURI(self, uri):
        """Delete all triples with the given URI as subject.
        """
        self._graph.remove((URIRef(uri), None, None))
        self._graph.commit()

    def deleteURILayer(self, layer):
        """Delete all URIs of the given layer.

        Args:
            layer(str): layer name. Available names:
                "Catalog", "Dataset", "Distribution".
        """
        self._graph.remove((None, None, DCAT[layer]))
        self._graph.commit()

    def navURI(self, layer):
        """Navigate existing URIs for given layer.

        Args:
            layer(str): layer name. Available names:
                "Catalog", "Dataset", "Distribution".

        Returns:
            list: URIs
        """
        qres = self._graph.subjects(object=DCAT[layer])
        return [s for s in qres]