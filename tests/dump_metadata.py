#
# This script creates dump files of metadata in different formats upon requests to FDP.
#

import os
import requests

from rdflib import Graph
from logging import getLogger, StreamHandler, INFO
from myglobals import *

logger = getLogger(__name__)
logger.setLevel(INFO)
ch = StreamHandler()
ch.setLevel(INFO)
logger.addHandler(ch)


def dump():
   for fmt,fxt in MIME_TYPES.items():
      dump_path = os.path.join(DUMP_DIR, os.path.basename(fmt))
      os.makedirs(dump_path)

      for url in [os.path.join(BASE_URL, p) for p in URL_PATHS]:
         logger.info("Request metadata in '%s' from %s\n" % (fmt, url))

         res = requests.get(url, headers={'Accept': fmt})
         fname = '%s.%s' % (os.path.basename(url), fxt)
         fname = os.path.join(dump_path, fname)

         logger.info("Write metadata into file './%s'\n" % fname)

         with open(fname, 'wb') as fout:
            fout.write(res.content)

if __name__ == "__main__":
   dump()
