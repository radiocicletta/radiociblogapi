#!/bin/env python

import urllib2
import json
import sys
import os


def harvest(path, idxname, **kwargs):

    base_url = "http://api.mixcloud.com"
    username = kwargs.get('username', '')
    if not username:
        return

    jsonidx = open("%s/%s.json" % (path, idxname), 'w')
    jsonidxobj = {"name": idxname, "playlists": {}}

    if not os.path.exists("%s/%s" % (path, idxname)):
        os.makedirs("%s/%s" % (path, idxname))

    try:
        result = urllib2.urlopen("%s/%s/playlists/?limit=1000&offset=0" % (base_url, username))
        playlists = json.loads(result.read())
    except:
        playlists = {"data": []}

    for plist in playlists["data"]:
        js = open("%s/%s/%s.json" % (path, idxname, plist['slug']), 'w')
        try:
            result = urllib2.urlopen("%s/%s/playlists/%s/cloudcasts/?limit=1000&offset=0" % (base_url, username, plist['slug']))
            js.write(result.read())
            jsonidxobj["playlists"][plist["slug"]] = "%s/%s.json" % (idxname, plist['slug'])
        except:
            pass
        finally:
            js.close()

    try:
        recents = urllib2.urlopen("%s/%s/cloudcasts/" % (base_url, username))
        jsonidxobj["recents"] = json.loads(recents.read())
    except:
        jsonidxobj["recents"] = {"data": []}

    jsonidx.write(json.dumps(jsonidxobj))
    jsonidx.close()

if __name__ == "__main__":
    if not len(sys.argv):
        sys.exit(0)

    path = sys.argv[1]
    idx = sys.argv[2]
    harvest(path, idx, username='radiocicletta')
