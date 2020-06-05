def _errorResourceNotFound(resource):
    return "Resource '%s' not found." % resource


# paths (endpoints) available through FDP
_RESOURCE_PATH = dict(fdp='/fdp',
                      doc='/doc',
                      cat='/catalog',
                      dat='/dataset',
                      dist='/distribution')

def FDPath(resource, var=None):
    assert(resource in _RESOURCE_PATH), _errorResourceNotFound(resource)
    path = _RESOURCE_PATH[resource]
    var = '' if var is None else '/%s' % str(var)

    return path + var
