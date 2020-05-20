curl -X GET "http://0.0.0.0:8080/fdp/" -H "accept: application/json"

curl -X POST "http://0.0.0.0:8080/catalog/" -H "accept: application/json" -H "Content-Type: application/json" -d '
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix fdp: <http://rdf.biosemantics.org/ontologies/fdp-o#> .
@prefix dbp: <http://dbpedia.org/resource/> .

<http://0.0.0.0:8080/catalog/catalog-01> a dcat:Catalog ;
    dcterms:title "Title" ;
    dcterms:hasVersion "1.0" ;
    dcterms:publisher <http://orcid.org/0000-0002-4368-8058> ;
    dcterms:isPartOf <fdp> ;

    fdp:metadataIdentifier <http://example.org/metadataID> ;
		fdp:metadataIssued "2016-10-27"^^xsd:date ;
		fdp:metadataModified "2016-10-27"^^xsd:date ;

    dcat:dataset <dataset/breedb> ;
    dcat:themeTaxonomy dbp:Breeding .
'
curl -X GET "http://0.0.0.0:8080/catalog/catalog-01" -H "accept: application/json"

curl -X POST "http://0.0.0.0:8080/dataset/" -H "accept: application/json" -H "Content-Type: application/json" -d '
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix fdp: <http://rdf.biosemantics.org/ontologies/fdp-o#> .
@prefix dbp: <http://dbpedia.org/resource/> .

<http://0.0.0.0:8080/dataset/breedb> a dcat:Dataset ;
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
'
curl -X GET "http://0.0.0.0:8080/dataset/breedb" -H "accept: application/json"

curl -X POST "http://0.0.0.0:8080/distribution/" -H "accept: application/json" -H "Content-Type: application/json" -d '
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix fdp: <http://rdf.biosemantics.org/ontologies/fdp-o#> .
@prefix dbp: <http://dbpedia.org/resource/> .

@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix lang: <http://id.loc.gov/vocabulary/iso639-1/> .

<http://0.0.0.0:8080/distribution/breedb-sparql> a dcat:Distribution ;
    dcterms:title "SPARQL endpoint for BreeDB tomato passport data"^^xsd:string ;
    dcterms:license <http://rdflicense.appspot.com/rdflicense/cc-by-nc-nd3.0> ;
    dcterms:hasVersion "1.0"^^xsd:string ;
    dcterms:isPartOf <dataset/breedb> ;

    fdp:metadataIdentifier <http://example.org/metadataID> ;
		fdp:metadataIssued "2016-10-27"^^xsd:date ;
		fdp:metadataModified "2016-10-27"^^xsd:date ;

    dcat:mediaType "application/n-triples"^^xsd:string,
        "application/rdf+xml"^^xsd:string ;

    dcat:accessURL <http://virtuoso.biotools.nl:8888/sparql> .
'
curl -X GET "http://0.0.0.0:8080/distribution/breedb-sparql" -H "accept: application/json"
