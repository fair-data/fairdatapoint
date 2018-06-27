DUMP_DIR = 'rdf-metadata'
BASE_URL = 'http://127.0.0.1:8080'

# example catalog, dataset and distributions
URL_PATHS = [
    'fdp',
    'catalog/astron-01',
    'dataset/lofar-lta-dbview',
    'distribution/lofar-lta-dbview-sparql',
    'distribution/lofar-lta-dbview-sqldump'
]

# lookup table: MIME type - file extension pairs
MIME_TYPES = {
    'text/turtle'           : 'ttl',
    'application/rdf+xml'   : 'rdf',
    'application/ld+json'   : 'jsonld',
    'application/n-triples' : 'nt'
}

