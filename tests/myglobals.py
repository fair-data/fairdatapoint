DUMP_DIR = 'tests/rdf-metadata'
BASE_URL = 'http://0.0.0.0:8080'

# example catalog, dataset and distributions
URL_PATHS = [
    'fdp',
    'catalog/pbg-ld',
    'dataset/sly-genes',
    'dataset/spe-genes',
    'dataset/stu-genes',
    'distribution/sly-genes-gff',
    'distribution/spe-genes-gff',
    'distribution/stu-genes-gff'
]

# lookup table: MIME type - file extension pairs
MIME_TYPES = {
    'text/turtle'           : 'ttl',
    'application/rdf+xml'   : 'rdf',
    'application/ld+json'   : 'jsonld',
    'application/n-triples' : 'nt'
}
