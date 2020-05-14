from rdflib import Graph
from .basegraph import BaseFAIRGraph

class FAIRGraph(BaseFAIRGraph):
    def __init__(self, base_uri, ttl_file):
        # UPGRADE: use rdflib.plugins.stores.sparqlstore.SPARQLStore
        # for SPARQL backend.
        self._graph = Graph()
        self._graph.parse(ttl_file, format="n3")
        super().__init__(base_uri)