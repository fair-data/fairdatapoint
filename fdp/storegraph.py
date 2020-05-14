from rdflib import Graph
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from rdflib.term import URIRef

from .basegraph import BaseFAIRGraph

class StoreFAIRGraph(BaseFAIRGraph):
    def __init__(self, base_uri, endpoint):
        default_graph = URIRef(base_uri)

        self._store = SPARQLUpdateStore(endpoint)
        self._graph = Graph(self._store, identifier=default_graph)
        super().__init__(base_uri)