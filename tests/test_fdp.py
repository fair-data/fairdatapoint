import os
import unittest
import requests

from rdflib import ConjunctiveGraph
from rdflib.compare import graph_diff
from rdflib.plugin import register, Parser
from .myglobals import (BASE_URL, DUMP_DIR, MIME_TYPES, URL_PATHS)

register('application/ld+json', Parser, 'rdflib_jsonld.parser', 'JsonLDParser')
URLs = [os.path.join(BASE_URL, p) for p in URL_PATHS]

g_fdp = ConjunctiveGraph() # FDP metadata upon HTTP request
g_dump = ConjunctiveGraph() # reference metadata from dump file

# TODO use urllib
# TODO input is ini and ttl, and output is different type

class Test_FDP(unittest.TestCase):

    def test_compare_triple_counts(self):
        for mime, fext in MIME_TYPES.items():
            dump_path = os.path.join(DUMP_DIR, os.path.basename(mime))

            for url in URLs:
                fname = '%s.%s' % (os.path.basename(url), fext)
                fname = os.path.join(dump_path, fname)

                # redirect for folders
                res = requests.get(url, headers={'Accept': mime})

                g_fdp.parse(data=res.content, format=mime)
                g_dump.parse(fname, format=mime)

                # triple counts
                nt_fdp, nt_dump = len(g_fdp), len(g_dump)
                self.assertEqual(
                nt_fdp, nt_dump, 'Triple counts differ: %d (FDP) vs. %d (ref)' % (nt_fdp, nt_dump))


    def test_compare_triples(self):
        for mime, fext in MIME_TYPES.items():
            dump_path = os.path.join(DUMP_DIR, os.path.basename(mime))

            for url in URLs:
                fname = '%s.%s' % (os.path.basename(url), fext)
                fname = os.path.join(dump_path, fname)

                res = requests.get(url, headers={'Accept': mime})

                g_fdp.parse(data=res.content, format=mime)
                g_dump.parse(fname, format=mime)

                both, first, second = graph_diff(g_fdp, g_dump)
                n_first = len(first)
                # n_second = len(second)
                # n_both = len(both)

                # TODO check it
                self.assertEqual(
                n_first, 0, '{} triple(s) different from reference:\n\n{}===\n{}\n'.format(
                    n_first, first.serialize(format='turtle'), second.serialize(format='turtle')))
