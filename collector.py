#!/bin/env python2.6
# the ubermaster social feeds collectr

import sys, os
import urllib2
try:
    import json
except:
    import simplejson as json

if __name__ == "__main__":
    if not len(sys.argv):
        sys.exit(0)

    path = sys.argv[1]
    jsonpath = sys.argv[2]
    try:
        request = urllib2.urlopen(jsonpath)
        jsonrequest = json.loads(request.read())
        modules = jsonrequest['modules']
        modules_args = jsonrequest['modules_args']
    except:
        modules = ['mixcloud', 'twitter', 'facebook']
        modules_args = { 'twitter':  { 'streams':['radiocicletta'] },
                         'mixcloud': { 'username':'radiocicletta'  },
                         'facebook': { 'items':['radiocicletta']  }}

    if not os.path.exists(path):
        os.makedirs(path, idxname)

    collect = open("%s/socialroot.json" % path, "w")
    collect.write('{')

    for i, module in enumerate(modules):
        try:
            mod = __import__(module)
            mod.harvest(path, module, **modules_args[module])
            if os.path.exists("%s/%s.json" % (path, module)):
                modfile = open("%s/%s.json" % (path, module), 'r')
                collect.write('%s"%s":' % ( i > 0 and ', ' or ' ', module))
                collect.write(modfile.read())
                modfile.close()
        except:
            pass

    collect.write('}')
    collect.close()
