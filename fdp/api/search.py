from flask import request, Response
import requests
from fdp.config import get_grlc_endpoint, get_sparql_endpoint

grlc_endpoint = get_grlc_endpoint()
sparql_endpoint = get_sparql_endpoint()

class MetaSearch():
    def get(text):
        rq_url = grlc_endpoint  + request.path +  '?' + request.query_string.decode() + '&endpoint=' + sparql_endpoint
        r = requests.get(rq_url, headers=request.headers)
        return Response(r.text,
                status=r.status_code,
                content_type=r.headers['Content-Type'])

FindText = MetaSearch()
FindURI = MetaSearch()
FindMediaType = MetaSearch()
FindPublisher = MetaSearch()
FindVersion = MetaSearch()
GetChildrenIDs = MetaSearch()
GetDataURLs = MetaSearch()
GetLicenses = MetaSearch()
GetMediaTypes = MetaSearch()
GetParentIDs = MetaSearch()
GetPublishers = MetaSearch()
GetThemeTaxonomy = MetaSearch()
GetThemes = MetaSearch()