import sys
import six

from nose.tools import (assert_equals, assert_true, assert_false)


# add parent folder to path
sys.path.append('../')
from metadata import (FAIRConfigReader, FAIRGraph)

if six.PY2:
    from urllib2 import urlparse
    urljoin = urlparse.urljoin
    urlparse = urlparse.urlparse
else:
    from urllib.parse import urljoin

reader = FAIRConfigReader()


def test_sections():
    set_a = set(['fdp', 'catalog/astron-01', 'dataset/lofar-lta-dbview',
                 'distribution/lofar-lta-dbview-sparql',
                 'distribution/lofar-lta-dbview-sqldump',
                 'distribution/lofar-lta-dbview-csvdump'])
    set_b = set(reader.getSectionHeaders())
    assert_true(set_a == set_b)


def test_get_items():
    for section, fields in reader.getMetadata().items():
        for field in fields:
            assert_false(isinstance(reader.getItems(section, field), list))


def test_get_triples():
    for triple in reader.getTriples():
        assert_true(isinstance(triple, tuple))
        assert_equals(len(triple), 3)


base_uri = 'http://127.0.0.1:8080'
g = FAIRGraph(base_uri)


def test_base_uri():
    assert_equals(base_uri, g.baseURI())


def test_doc_uri():
    assert_equals(urljoin(base_uri, 'doc'), g.docURI())


def test_fdp_uri():
    assert_equals(urljoin(base_uri, 'fdp'), g.fdpURI())


def test_catalog_uri():
    assert_equals(urljoin(base_uri, 'catalog/astron-01'),
                  g.catURI('astron-01'))


def test_dataset_uri():
    assert_equals(urljoin(base_uri, 'dataset/lofar-lta-dbview'),
                  g.datURI('lofar-lta-dbview'))


def test_distribution_uri():
    assert_equals(urljoin(base_uri, 'distribution/lofar-lta-dbview-sparql'),
                  g.distURI('lofar-lta-dbview-sparql'))


def test_distribution_uri():
    assert_equals(urljoin(base_uri, 'distribution/lofar-lta-dbview-sqldump'),
                  g.distURI('lofar-lta-dbview-sqldump'))


def test_distribution_uri():
    assert_equals(urljoin(base_uri, 'distribution/lofar-lta-dbview-csvdump'),
                  g.distURI('lofar-lta-dbview-csvdump'))
