import pkg_resources

from pyshacl import validate
from rdflib.graph import Graph

def _validate(data, shapes_file, fdp=False):
    try:
        data_format = 'turtle'
        shapes_file_format = 'turtle'
        # validate number of subjects or focus nodes
        g = Graph()
        g.parse(data=data, format=data_format)
        s_set = set([s for s, p, o in g])
        if len(s_set) == 0:
            raise ValueError('Empty content in metadtata')
        elif len(s_set) > 1 and fdp:
            raise ValueError('FDP layer allows only one subject in metadata')
            print('fdp only allow one subject')
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
        print('Loading fdp shapes')
        self.fdp_shapes = pkg_resources.resource_string(__name__, 'schema/fdp.shacl')
        print('Loading catalog shapes')
        self.catalog_shapes = pkg_resources.resource_string(__name__, 'schema/catalog.shacl')
        print('Loading dataset shapes')
        self.dataset_shapes = pkg_resources.resource_string(__name__, 'schema/dataset.shacl')
        print('Loading distribution shapes')
        self.distribution_shapes = pkg_resources.resource_string(__name__, 'schema/distribution.shacl')

    def validateFDP(self, data):
        return _validate(data, self.fdp_shapes, fdp=True)

    def validateCatalog(self, data):
        return _validate(data, self.catalog_shapes)

    def validateDataset(self, data):
        return _validate(data, self.dataset_shapes)

    def validateDistribution(self, data):
        return _validate(data, self.distribution_shapes)
