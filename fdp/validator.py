from pyshacl import validate

def _validate(data_file, shapes_file):
    try:
        data_file_format = 'turtle'
        shapes_file_format = 'turtle'
        conforms, v_graph, v_text = validate(data_file, shacl_graph=shapes_file,
                                             data_graph_format=data_file_format,
                                             shacl_graph_format=shapes_file_format,
                                             inference='rdfs', debug=False,
                                             serialize_report_graph=True)
        return conforms
    except:
        print('There was an exception!')
        return False


class FDPValidator():
    def __init__(self):
        print('Loading catalog shapes')
        with open('fdp/schema/catalog.shacl') as fin:
            self.catalog_shapes = fin.read()
        print('Loading dataset shapes')
        with open('fdp/schema/dataset.shacl') as fin:
            self.dataset_shapes = fin.read()
        print('Loading distribution shapes')
        with open('fdp/schema/distribution.shacl') as fin:
            self.distribution_shapes = fin.read()

    def validateCatalog(self, cat_data):
        return _validate(cat_data, self.catalog_shapes)

    def validateDataset(self, cat_data):
        return _validate(cat_data, self.dataset_shapes)

    def validateDistribution(self, cat_data):
        return _validate(cat_data, self.distribution_shapes)
