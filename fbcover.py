#!/bin/env python

import hammock
import urllib2
import re
import sys
import math
from random import shuffle
from random import sample
from random import choice
from StringIO import StringIO
from PIL import Image
from PIL.ImageDraw import ImageDraw
from tilify import Rectangle, guillotine_baf_las, depth_composite


def getalbums(**kwargs):
    items = kwargs.get('items', [])
    app_id = kwargs.get('app_id', '')
    app_secret = kwargs.get('app_secret', '')
    try:
        oauth = urllib2.urlopen(
            'https://graph.facebook.com/oauth/access_token?'
            'client_id=%s&client_secret=%s&grant_type=client_credentials' %
            (app_id, app_secret))
        txt = oauth.read()
        access_token = re.search('access_token=(.*)', txt).groups()[0]
    except:
        sys.exit(0)

    facebook = hammock.Hammock("https://graph.facebook.com")

    # 851 315
    # 840 300
    # 120 100

    images = []
    for item in items:
        try:
            metadata = facebook.__getattr__(item).GET(
                "", params={"access_token": access_token}
            ).json()
            feed = facebook.__getattr__(metadata['id']).GET(
                "albums", params={"access_token": access_token}
            ).json()
            filtered = [
                i for i in feed['data']
                if not i['name']
                in (
                    u'Profile Pictures',
                    u'Cover Photos',
                    u'Timeline Photos'
                )]
            shuffle(filtered)
            for album in filtered:
                photos = facebook.__getattr__(album['id']).GET(
                    "photos", params={"access_token": access_token}
                ).json()
                shuffle(photos['data'])
                chosen = sample(
                    photos['data'],
                    choice(range(1, int(math.ceil(len(filtered) ** 0.5))))
                )
                for c in chosen:
                    print "processing", c['source']
                    try:
                        data = StringIO(urllib2.urlopen(c['source']).read())
                        img = Image.open(data)
                        if choice((0, 1)):
                            img = img.resize((
                                img.size[0] / 2,
                                img.size[1] / 2),
                                Image.ANTIALIAS)
                        if img.size[0] < img.size[1]:  # portrait
                            img = img.crop((
                                max(img.size[0] / 2 - 120 * choice((1, 2)), 0),
                                max(img.size[1] / 2 - 105 * choice((1, 2, 3)), 0),
                                img.size[0] / 2 + 120,
                                img.size[1] / 2 + 105,
                            ))
                        else:  # landscape
                            img = img.crop((
                                max(img.size[0] / 2 - 120 * choice((1, 2, 3)), 0),
                                max(img.size[1] / 2 - 105 * choice((1, 2)), 0),
                                img.size[0] / 2 + 120,
                                img.size[1] / 2 + 105,
                            ))
                        draw = ImageDraw(img)
                        draw.rectangle(
                            [1, 1,
                             img.size[0] - 2, img.size[1] - 2],
                            outline="white"
                        )
                        draw.rectangle(
                            [0, 0,
                             img.size[0] - 1, img.size[1] - 1],
                            outline="white"
                        )
                        images.append(
                            Rectangle(
                                0, 0,
                                img.size[0],
                                img.size[1],
                                img
                            ))
                    except:
                        pass
        except:
            sys.exit(0)

        container = Rectangle(
            0, 0,
            1440, 500,
            Image.open("template.png"))

        guillotine_baf_las(container, images)
        depth_composite(container, container, 0, 0)
        offset = choice(tuple(i for i in range(0, 100, 10)))
        crop = container.image.crop((
            offset, offset,
            851 + offset, 315 + offset
        ))
        draw = ImageDraw(crop)
        draw.rectangle(
            (0, 0,
             crop.size[0] - 1,
             crop.size[1] - 1),
            outline="white"
        )
        draw.rectangle(
            (1, 1,
             crop.size[0] - 2,
             crop.size[1] - 2),
            outline="white"
        )
        crop.save(open("result.png", "w"))


if __name__ == "__main__":
    if not len(sys.argv):
        sys.exit(0)

    app_id = sys.argv[1]
    app_secret = sys.argv[2]
    getalbums(
        items=['radiocicletta'],
        app_id=app_id,
        app_secret=app_secret
    )
