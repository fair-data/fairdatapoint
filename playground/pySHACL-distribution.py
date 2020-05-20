from pyshacl import validate

# This should be loaded from a file: fdp/schema/catalog.shacl or something
with open('distribution.shacl') as fin:
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

@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix lang: <http://id.loc.gov/vocabulary/iso639-1/> .

<distribution/breedb-sparql> a dcat:Distribution ;
    dcterms:title "SPARQL endpoint for BreeDB tomato passport data"^^xsd:string ;
    dcterms:license <http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0> ;
    dcterms:hasVersion "1.0"^^xsd:string ;
    dcterms:isPartOf <dataset/breedb> ;

    fdp:metadataIdentifier <http://example.org/metadataID> ;
	fdp:metadataIssued "2016-10-27"^^xsd:date ;
	fdp:metadataModified "2016-10-27"^^xsd:date ;

    dcat:mediaType "application/n-triples"^^xsd:string,
        "application/rdf+xml"^^xsd:string ;

    # One or the other, but not both
    dcat:accessURL <http://virtuoso.biotools.nl:8888/sparql> .
    # dcat:downloadURL <http://virtuoso.biotools.nl:8888/sparql>  .
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
