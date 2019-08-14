#
# This script creates dump files of metadata in different formats upon requests to FDP.
#

import os
import six

from rdflib import Graph
from logging import getLogger, StreamHandler, INFO
from myglobals import *

if six.PY2:
    from urllib2 import (urlopen, urlparse, Request)
    urljoin = urlparse.urljoin
    urlparse = urlparse.urlparse
else:
    from urllib.request import (Request, urlopen, urlparse)
    from urllib.parse import urljoin

logger = getLogger(__name__)
logger.setLevel(INFO)
ch = StreamHandler()
ch.setLevel(INFO)
logger.addHandler(ch)


def dump():
   for fmt,fxt in MIME_TYPES.items():
      dump_path = os.path.join(DUMP_DIR, os.path.basename(fmt))
      os.makedirs(dump_path)

      for url in [urljoin(BASE_URL, p) for p in URL_PATHS]:
         logger.info("Request metadata in '%s' from %s\n" % (fmt, url))

         req = Request(url)
         req.add_header('Accept', fmt)
         res = urlopen(req)
         fname = '%s.%s' % (os.path.basename(urlparse(url).path), fxt)
         fname = os.path.join(dump_path, fname)

         logger.info("Write metadata into file './%s'\n" % fname)

         with open(fname, 'wb') as fout:
            fout.write(res.read())

dump()

