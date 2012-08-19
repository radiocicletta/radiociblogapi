#!/bin/env python

import hammock
import json
import urllib2
import re
import sys, os

def harvest(path, idxname, **kwargs):

    items = kwargs.get('items', [])
    access_token = kwargs.get('access_token', '')
    if not access_token: # this IS a real trick. Hope you don't mind if i steal some tokens.
        try:
            zesty = urllib2.urlopen('http://zesty.ca/facebook')
            txt = zesty.read()
            access_token = re.search('id="token"\s+value="(\w*)"', txt).groups()[0]
        except:
            pass

    facebook = hammock.Hammock("https://graph.facebook.com")

    jsonidx = open("%s/%s.json" % (path, idxname), 'w')
    jsonidxobj = { "name": idxname, "items":{}, "latest":[] }

    if not os.path.exists("%s/%s" % (path, idxname)):
        os.makedirs("%s/%s" % (path, idxname))

    for item in items:
        js = open("%s/%s/%s.json" % (path, idxname, item), 'w')
        try:
            metadata = facebook.__getattr__(item).GET("", params={"access_token": access_token}).json
            feed = facebook.__getattr__(metadata['id']).GET("feed", params={"access_token": access_token}).json
            filtered = filter(lambda x: x['from']['id'] == metadata['id'], feed['data'])
            filtered.sort(lambda x, y: x['created_time'] > y['created_time'])
            js.write(json.dumps(filtered))
            jsonidxobj['items'][item] = "%s/%s.json" % (idxname, item)
            if len(filtered):
                jsonidxobj['latest'].append(filtered[0])
        except:
            pass
        finally:
            js.close()

    jsonidx.write(json.dumps(jsonidxobj))
    jsonidx.close()


if __name__ == "__main__":
    if not len(sys.argv):
        sys.exit(0)

    path = sys.argv[1]
    idx = sys.argv[2]
    access_token = sys.argv[3]
    harvest(path, idx, items=['radiocicletta'], access_token=access_token)
