#!/bin/env python

import hammock
import json
import sys, os

def harvest(path, idxname, **kwargs):

    streams = kwargs.get('streams', [])
    twitter = hammock.Hammock("https://api.twitter.com/1")

    jsonidx = open("%s/%s.json" % (path, idxname), 'w')
    jsonidxobj = { "name": idxname, "tweets":{}, "latest":[] }

    if not os.path.exists("%s/%s" % (path, idxname)):
        os.makedirs("%s/%s" % (path, idxname))

    for stream in streams:
        js = open("%s/%s/%s.json" % (path, idxname, stream), 'w')
        try:
            tweets = twitter.statuses('user_timeline.json').GET(params={'screen_name':stream, 'count':'5'}).json
            tweets.sort(lambda x,y: x['created_at'] > y['created_at'])
            js.write(json.dumps(tweets))
            jsonidxobj['tweets'][stream] = "%s/%s.json" % (idxname, stream)
            if len(tweets):
                jsonidxobj['latest'].append(tweets[0])
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
    harvest(path, idx, streams=['radiocicletta'])
