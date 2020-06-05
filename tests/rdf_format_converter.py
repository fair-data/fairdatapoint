#!/usr/bin/env python3
"""RDF format converter.

Mainly internal use to prepare test sample files from '.ttl' files.
"""

from os import path
from rdflib import Graph

def rdf_converter(fin, fin_format, fout, fout_format):
    g = Graph()
    g.parse(fin, format=fin_format)
    g.serialize(fout, format=fout_format)

def main():
    fmt2ext = {
        'n3': '.n3',
        'nt': '.nt',
        'turtle': '.ttl',
        'xml': '.rdf',
        'json-ld': '.jsonld'
    }
    fnames = ["fdp", "catalog01", "catalog02", "dataset01", "dataset02", "dist01", "dist02" ]
    cwd = path.dirname(path.abspath(__file__))
    fpaths = [cwd + '/data/' + i for i in fnames]

    infmt = 'turtle'
    outfmts = ['n3', 'nt', 'xml', 'json-ld']
    print('Generated files:')
    for ofmt in outfmts:
        for i in fpaths:
            rdf_converter(i + fmt2ext[infmt], infmt, i + fmt2ext[ofmt], ofmt)
            print(i+fmt2ext[ofmt])

if __name__ == "__main__":
    main()