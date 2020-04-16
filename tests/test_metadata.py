import sys
import unittest
from urllib.parse import urljoin

from fdp.metadata import (FAIRConfigReader, FAIRGraph)

class Test_FAIRConfigReader(unittest.TestCase):

    def setUp(self):
        datafile = 'samples/config.ini'
        self.reader = FAIRConfigReader(datafile)

    def test_sections(self):
        set_a = set([
            'fdp',
            'catalog/pbg-ld',
            'dataset/sly-genes',
            'dataset/spe-genes',
            'dataset/stu-genes',
            'distribution/sly-genes-gff',
            'distribution/spe-genes-gff',
            'distribution/stu-genes-gff'])

        set_b = set(self.reader.getSectionHeaders())
        self.assertEqual(set_a, set_b)


    def test_get_items(self):
        for section, fields in self.reader.getMetadata().items():
            for field in fields:
                self.assertFalse(isinstance(self.reader.getItems(section, field), list))

    def test_get_triples(self):
        for triple in self.reader.getTriples():
            self.assertTrue(isinstance(triple, tuple))
            self.assertEqual(len(triple), 3)

class Test_FAIRGraph(unittest.TestCase):

    def setUp(self):

        self.base_uri = 'http://127.0.0.1:8080'
        self.g = FAIRGraph(self.base_uri)

    def test_base_uri(self):
        self.assertEqual(self.base_uri, self.g.baseURI())

    def test_doc_uri(self):
        self.assertEqual(urljoin(self.base_uri, 'doc'), self.g.docURI())


    def test_fdp_uri(self):
        self.assertEqual(urljoin(self.base_uri, 'fdp'), self.g.fdpURI())


    def test_catalog_uri(self):
        self.assertEqual(urljoin(self.base_uri, 'catalog/astron-01'),
                    self.g.catURI('astron-01'))


    def test_dataset_uri(self):
        self.assertEqual(urljoin(self.base_uri, 'dataset/lofar-lta-dbview'),
                    self.g.datURI('lofar-lta-dbview'))


    def test_distribution_uri_01(self):
        self.assertEqual(urljoin(self.base_uri, 'distribution/lofar-lta-dbview-sparql'),
                    self.g.distURI('lofar-lta-dbview-sparql'))


    def test_distribution_uri_02(self):
        self.assertEqual(urljoin(self.base_uri, 'distribution/lofar-lta-dbview-sqldump'),
                    self.g.distURI('lofar-lta-dbview-sqldump'))


    def test_distribution_uri_03(self):
        self.assertEqual(urljoin(self.base_uri, 'distribution/lofar-lta-dbview-csvdump'),
                    self.g.distURI('lofar-lta-dbview-csvdump'))
