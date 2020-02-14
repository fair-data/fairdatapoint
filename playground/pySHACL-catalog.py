from pyshacl import validate

# This should be loaded from a file: fdp/schema/catalog.shacl or something
with open('catalog.shacl') as fin:
    shapes_file = fin.read()
shapes_file_format = 'turtle'

# This data should be posted
data_file = '''
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .


@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix fdp: <http://rdf.biosemantics.org/ontologies/fdp-o#> .
@prefix dbp: <http://dbpedia.org/resource/> .

<catalog/catalog-01> a dcat:Catalog ;
    dct:title "Title" ;
    dct:hasVersion "1.0" ;
    dct:publisher <http://orcid.org/0000-0002-4368-8058> ;

    fdp:metadataIdentifier <http://example.org/metadataID> ;
	fdp:metadataIssued "2016-10-27"^^xsd:date ;
	fdp:metadataModified "2016-10-27"^^xsd:date ;

    dcat:dataset <dataset/breedb> ;
    dcat:themeTaxonomy dbp:Breeding .
'''
data_file_format = 'turtle'


conforms, v_graph, v_text = validate(data_file, shacl_graph=shapes_file,
                                     data_graph_format=data_file_format,
                                     shacl_graph_format=shapes_file_format,
                                     inference='rdfs', debug=False,
                                     serialize_report_graph=True)
print('conforms >>>>>>>>>>>>>>>>>')
print(conforms)
print('v_graph >>>>>>>>>>>>>>>>>>')
print(v_graph)
print('v_text >>>>>>>>>>>>>>>>>>>')
print(v_text)
