from abc import ABC, abstractmethod
from rdflib import Graph, Namespace
from rdflib.term import URIRef

API_ENDPOINTS = {'/fdp', '/doc', '/catalog/', '/dataset/', '/distribution/'}
DCAT = Namespace("http://www.w3.org/ns/dcat#")

class BaseFAIRGraph(ABC):
    @abstractmethod
    def __init__(self, base_uri):
        self._base_uri = base_uri

    def _buildURI(self, endpoint, id=None):
        assert (endpoint in API_ENDPOINTS), 'Invalid endpoint'
        id = '' if id is None else '%s' % str(id)
        return self._base_uri + endpoint + id

    def fdpURI(self):
        return self._buildURI('/fdp')

    def catURI(self, id=None):
        return self._buildURI('/catalog/', id)

    def datURI(self, id=None):
        return self._buildURI('/dataset/', id)

    def distURI(self, id=None):
        return self._buildURI('/distribution/', id)

    def serialize(self, uri, mime_type):
        # TODO mime_type not used
        g = self.matchURI(uri)
        if len(g.all_nodes()) > 0:
            return g.serialize(format='turtle').decode('utf-8')
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
            # Add new triples
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
        # for i in self.navURI(layer):
        #     self.deleteURI(i)

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