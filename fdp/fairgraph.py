from rdflib import ConjunctiveGraph, Graph
from rdflib.term import URIRef

from .basegraph import BaseFAIRGraph

from rdflib import Namespace
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class FAIRGraph(BaseFAIRGraph):
    def __init__(self, base_uri, ttl_file):
        # UPGRADE: use rdflib.plugins.stores.sparqlstore.SPARQLStore
        # for SPARQL backend.
        self._graph = ConjunctiveGraph()
        self._graph.parse(ttl_file, format="n3")
        super().__init__(base_uri)

    def addCatURI(self, data, format):
        self._graph.parse(data=data, format=format)

    def serialize(self, uri, mime_type):
        g = Graph()
        # Copy namespaces from base graph
        for prefix, ns_uri in self._graph.namespaces():
            g.bind(prefix, ns_uri)

        # Search for triples which match the given subject
        matchPattern = (URIRef(uri), None, None)
        g += self._graph.triples(matchPattern)

        if len(g.all_nodes()) > 0:
            return g.serialize(format='turtle').decode('utf-8')
        else:
            return None  # 404 !

    def post(self, data, format):
        """Overwrite all existing triples of a specific subject.
        """
        # Load data on the graph
        g = ConjunctiveGraph()
        g.parse(data=data, format=format)
        # Remove all triples of specific subjects
        s_set = set([s for s, p, o in g])
        if s_set:
            for s in s_set:
                self._graph.remove((s, None, None))
        # Add new triples
        for s, p, o in g:
            self._graph.add((s, p, o))
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

    def URIexists(self, uri):
        return (URIRef(uri), None, None) in self._graph

    def deleteURI(self, uri):
        """Delete all triples with the given URI as subject.
        """
        # remove all triples matching uri
        self._graph.remove((URIRef(uri), None, None))

    def deleteURILayer(self, layer):
        """Delete all URIs of the given layer.

        Args:
            layer(str): layer name. Available names:
                "Catalog", "Dataset", "Distribution".
        """
        pass
