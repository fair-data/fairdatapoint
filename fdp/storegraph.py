from rdflib import ConjunctiveGraph, Graph, Namespace
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from rdflib.term import URIRef

from .basegraph import BaseFAIRGraph


class StoreFAIRGraph(BaseFAIRGraph):
    def __init__(self, base_uri, endpoint):
        default_graph = URIRef(base_uri)

        self._store = SPARQLUpdateStore(endpoint)
        self._graph = Graph(self._store, identifier=default_graph)
        super().__init__(base_uri)

    def serialize(self, uri, mime_type):
        # TODO mime_type not used
        g = self.matchURI(uri)
        if len(g.all_nodes()) > 0:
            return g.serialize(format='turtle').decode('utf-8')
        else:
            return None  # 404 !

    def URIexists(self, uri):
        g = self.matchURI(uri)

        if len(g.all_nodes()) > 0:
            return True
        else:
            return False

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
        # self._graph.processUpdate(
        for i in self.navURI(layer):
            self.deleteURI(i)
        # self._graph.update(
        #     'DELETE {?s ?p ?o} WHERE {?s a ?l}',
        #     initBindings={'l': DCAT[layer]}
        #     )

    def navURI(self, layer):
        """Navigate existing URIs for given layer.

        Args:
            layer(str): layer name. Available names:
                "Catalog", "Dataset", "Distribution".

        Returns:
            list: URIs
        """
        qres = self._graph.query(
            'SELECT ?s, ?l WHERE {?s a ?l}',
            initBindings={'l': DCAT[layer]}
            )
        return [row.s for row in qres]
