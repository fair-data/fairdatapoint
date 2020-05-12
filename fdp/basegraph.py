from abc import ABC, abstractmethod

from rdflib import ConjunctiveGraph, Graph, Namespace
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from rdflib.term import URIRef

API_ENDPOINTS = {'/fdp', '/doc', '/catalog/', '/dataset/', '/distribution/'}
DCAT = Namespace("http://www.w3.org/ns/dcat#")


# BaseFAIRGraph must include:
# app.graph.fdpURI()
# app.graph.catURI()
# app.graph.datURI()
# app.graph.distURI()
# instance specific
# app.graph.post()
# app.graph.URIexists()
# app.graph.deleteURI()
# app.graph.deleteURILayer()
# app.graph.serialize(format='turtle').decode('utf-8')
# TODO: 
# graph.navURI(layer) -- abstract from fairgraph and storegraph

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

    @abstractmethod
    def serialize(self, uri, mime_type):
        pass

    @abstractmethod
    def URIexists(self, uri):
        pass

    @abstractmethod
    def post(self, data, format):
        """Overwrite all existing triples of a specific subject.
        """
        pass

    @abstractmethod
    def deleteURI(self, uri):
        """Delete all triples with the given URI as subject.
        """
        pass

    @abstractmethod
    def deleteURILayer(self, layer):
        """Delete all URIs of the given layer.

        Args:
            layer(str): layer name. Available names:
                "Catalog", "Dataset", "Distribution".
        """
        pass

    @abstractmethod
    def navURI(self, layer):
        """Navigate existing URIs for given layer.

        Args:
            layer(str): layer name. Available names:
                "Catalog", "Dataset", "Distribution".

        Returns:
            list: URIs
        """
        pass
