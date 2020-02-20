import pkg_resources

from pyshacl import validate
from rdflib.graph import Graph

def _validate(data_file, shapes_file):
    try:
        data_file_format = 'turtle'
        shapes_file_format = 'turtle'
        g = Graph()
        g.parse(data=data_file, format=data_file_format)
        conforms, v_graph, v_text = validate(data_file, shacl_graph=shapes_file,
                                             data_graph_format=data_file_format,
                                             shacl_graph_format=shapes_file_format,
                                             inference='rdfs', debug=False,
                                             serialize_report_graph=True)
        return conforms, v_text
    except Exception as e:
        return False, e.message


class FDPValidator():
    def __init__(self):
        print('Loading catalog shapes')
        self.catalog_shapes = pkg_resources.resource_string(__name__, 'schema/catalog.shacl')
        print('Loading dataset shapes')
        self.dataset_shapes = pkg_resources.resource_string(__name__, 'schema/dataset.shacl')
        print('Loading distribution shapes')
        self.distribution_shapes = pkg_resources.resource_string(__name__, 'schema/distribution.shacl')

    def validateCatalog(self, cat_data):
        return _validate(cat_data, self.catalog_shapes)

    def validateDataset(self, cat_data):
        return _validate(cat_data, self.dataset_shapes)

    def validateDistribution(self, cat_data):
        return _validate(cat_data, self.distribution_shapes)
