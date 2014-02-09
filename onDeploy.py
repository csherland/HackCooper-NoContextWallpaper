from app import *

import os
import pprint

from google.appengine.api import memcache
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.ext import db
import urllib
import logging
from app import *
# pprint.pprint(os.environ.copy())

f = open('photolinks.txt','r')
#x=eval(f.read())
x = f.readlines()

#for line in x:
#    line

if True:
    query = BackgroundImage.all(keys_only=True)
    entries =query.fetch(1000)
    db.delete(entries)

if True:
    for i in range(len(x)):
        #link = urllib.quote_plus(link)
        b = BackgroundImage()
        b.url = x[i]
        b.put()

import json
if True:
    y = open('quotes.json','r')
    y = y.read()
    y = json.loads(y)
    for x in y:
        z = Quote()
        z.quote = x['quote']
        z.author = x['author']
        z.put()
