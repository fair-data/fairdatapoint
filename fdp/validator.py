import pkg_resources
from pyshacl import validate
from rdflib import Graph, RDF, Namespace

DCAT = Namespace('http://www.w3.org/ns/dcat#')
R3D = Namespace('http://www.re3data.org/schema/3-0#')
LAYER2TYPE  = {
    'FDP': R3D.Repository,
    'Catalog': DCAT.Catalog,
    'Dataset': DCAT.Dataset,
    'Distribution': DCAT.Distribution
    }

def _validate(data, data_format, layer, shapes_file):
    try:
        # validate mime type
        pyshacl_allowed_formats = ['turtle', 'xml', 'json-ld', 'nt', 'n3']
        if data_format not in pyshacl_allowed_formats:
            raise ValueError(f'Not allowed metadata format {data_format}. '
                        f'Recommended formats: {pyshacl_allowed_formats}.')

        # validate required subject type and the number of such subjects
        g = Graph()
        g.parse(data=data, format=data_format)
        s_set = set(g.triples((None, RDF.type, LAYER2TYPE[layer])))
        spo_set = set(g.triples((None, None, None)))
        if len(s_set) == 0:
            raise ValueError(
                f'Not found subject with required RDF type {LAYER2TYPE[layer]}.')
        elif len(s_set) > 1 and layer == 'FDP':
            raise ValueError(
                f'FDP layer allows only one subject with RDF type {LAYER2TYPE[layer]},'
                f' {len(s_set)} such subjects {s_set} were found.')

        # validate unwanted subject types, avoid mixing metadata of different layers
        for i in LAYER2TYPE.values():
            if i != LAYER2TYPE[layer] and (None, RDF.type, i) in g:
                raise ValueError(
                    f'Not allowed RDF type for layer {layer}: {LAYER2TYPE[layer]}.')

        # validate SHACL shapes
        conforms, v_graph, v_text = validate(data, shacl_graph=shapes_file,
                                             data_graph_format=data_format,
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=False,
                                             serialize_report_graph=True)
        return conforms, v_text
    except Exception as e:
        return False, e.args[0]


class FDPValidator():
    def __init__(self):
        self.fdp_shapes = pkg_resources.resource_string(__name__, 'schema/fdp.shacl')
        self.catalog_shapes = pkg_resources.resource_string(__name__, 'schema/catalog.shacl')
        self.dataset_shapes = pkg_resources.resource_string(__name__, 'schema/dataset.shacl')
        self.distribution_shapes = pkg_resources.resource_string(__name__, 'schema/distribution.shacl')

    def validate(self, data, format, layer):
        layer2shape = {
            'FDP': self.fdp_shapes,
            'Catalog': self.catalog_shapes,
            'Dataset': self.dataset_shapes,
            'Distribution': self.distribution_shapes
            }
        return _validate(data, format, layer, layer2shape[layer])