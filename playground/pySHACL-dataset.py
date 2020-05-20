from pyshacl import validate

# This should be loaded from a file: fdp/schema/dataset.ttl or something
with open('dataset.shacl') as fin:
    shapes_file = fin.read()
shapes_file_format = 'turtle'

# This data should be posted
data_file = '''
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix fdp: <http://rdf.biosemantics.org/ontologies/fdp-o#> .
@prefix dbp: <http://dbpedia.org/resource/> .

<dataset/breedb> a dcat:Dataset ;
    dcterms:title "BreeDB tomato passport data"^^xsd:string ;
    dcterms:publisher <http://orcid.org/0000-0002-4368-8058> ;
    dcterms:hasVersion "1.0"^^xsd:string ;
    dcterms:isPartOf <catalog/catalog-01> ;

    fdp:metadataIdentifier <http://example.org/metadataID> ;
	fdp:metadataIssued "2016-10-27"^^xsd:date ;
	fdp:metadataModified "2016-10-27"^^xsd:date ;

    dcat:distribution <distribution/breedb-sparql>,
        <distribution/breedb-sqldump> ;
    dcat:theme dbp:Plant_breeding .
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
