import pkg_resources
from pyshacl import validate
from rdflib import Graph, RDF, Namespace

DCAT = Namespace('http://www.w3.org/ns/dcat#')
R3D = Namespace('http://www.re3data.org/schema/3-0#')
LAYER2TYPE  = {
    'fdp': R3D.Repository,
    'catalog': DCAT.Catalog,
    'dataset': DCAT.Dataset,
    'distribution': DCAT.Distribution
    }

def _validate(data, shapes_file, layer):
    try:
        data_format = 'turtle'
        shapes_file_format = 'turtle'
        # validate number of subjects or focus nodes
        g = Graph()
        g.parse(data=data, format=data_format)
        s_set = set([s for s, p, o in g])
        if len(s_set) == 0:
            raise ValueError('Empty content in metadata')
        elif len(s_set) > 1 and layer=='fdp':
            raise ValueError('FDP layer allows only one subject in metadata')

        # validate RDF.type
        if (None, RDF.type, LAYER2TYPE[layer]) not in g:
            raise ValueError(f'Not found required RDF type {LAYER2TYPE[layer]} in metadata')

        # validate SHACL shapes
        conforms, v_graph, v_text = validate(data, shacl_graph=shapes_file,
                                             data_graph_format=data_format,
                                             shacl_graph_format=shapes_file_format,
                                             inference='rdfs', debug=False,
                                             serialize_report_graph=True)
        return conforms, v_text
    except ValueError as e:
        return False, e.args[0]
    except Exception as e:
        return False, e.message


class FDPValidator():
    def __init__(self):
        self.fdp_shapes = pkg_resources.resource_string(__name__, 'schema/fdp.shacl')
        self.catalog_shapes = pkg_resources.resource_string(__name__, 'schema/catalog.shacl')
        self.dataset_shapes = pkg_resources.resource_string(__name__, 'schema/dataset.shacl')
        self.distribution_shapes = pkg_resources.resource_string(__name__, 'schema/distribution.shacl')

    def validateFDP(self, data):
        return _validate(data, self.fdp_shapes, layer='fdp')

    def validateCatalog(self, data):
        return _validate(data, self.catalog_shapes, layer='catalog')

    def validateDataset(self, data):
        return _validate(data, self.dataset_shapes, layer='dataset')

    def validateDistribution(self, data):
        return _validate(data, self.distribution_shapes, layer='distribution')
