import logging
import string
import webapp2
import json
import jinja2
import os
import datetime
import urllib2
import urllib

from google.appengine.api import channel
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import images

from nocontext.addText import addText

import random
logging.getLogger().setLevel(logging.DEBUG)
import sys
for attr in ('stdin', 'stdout', 'stderr'):
    setattr(sys, attr, getattr(sys, '__%s__' % attr))

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class BackgroundImage(db.Model):
    url = db.StringProperty(multiline=True)
    rand_int = db.IntegerProperty()

class Font(db.Model):
    font = db.StringProperty()
    rand_int = db.IntegerProperty()

class Post(db.Model):
    image = db.BlobProperty()
    #image = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    quote = db.StringProperty(multiline=True)
    #font = db.ReferenceProperty(Font)
    #background = db.ReferenceProperty(BackgroundImage)
    author = db.StringProperty(multiline=True)

class Quote(db.Model):
    quote = db.StringProperty(multiline=True)
    author = db.StringProperty(multiline=True)
    rand_int = db.IntegerProperty()

#class Upload(blobstore_handlers.BlobstoreUploadHandler):
#    def post(self):
#        post = Post()
#        post.image = self.request.get('image')
#        post.quote = self.request.get('quote')
#        post.font = self.request.get('font')
#        post.background = self.request.get('background')
#
#        upload_files = self.get_uploads('img')  # 'file' is file upload field in the form
#        if upload_files:
#            blob_info = upload_files[0]
#            image = blob_info.key() #self.request.get('img')
#            post.image = images.get_serving_url(image)
#        post.put()
#        self.redirect('/')

class Update(webapp2.RequestHandler):

    def get(self):
        posts = self.request.get('posts')

class UserPost(webapp2.RequestHandler):
#class Upload(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        # TODO: random quote if random button hit, otherwise do user quote
        author = self.request.get('author')
        quote = self.request.get('quote')

        # get random background
        max_bg = db.GqlQuery('SELECT rand_int FROM BackgroundImage ORDER BY rand_int DESC LIMIT 1').get().rand_int
        rand_int = random.randint(1,max_bg)
        bg_url = db.GqlQuery('SELECT * FROM BackgroundImage WHERE rand_int=%s' % rand_int).get().url

        # overlay text
        img_out = addText(quote, author, bg_url)
        #img_out = '01'

        # save in datastore / blobstore
        # upload_url = blobstore.create_upload_url('/upload')
        p = Post(
                image=img_out,
                author=author,
                quote=quote
                )
        p.put()

        # send message thru channel api
        key = p.key()

        datHash = 'thisIsOurHashAndShit'
        channel.send_message(datHash,json.dumps({'key':str(p.key())}))

        self.redirect('/')

        #params = {"author":author,
        #        "quote":quote,
        #        "img":img_out
        #        }
        #encd = urllib.urlencode(params)
        #req = urllib2.Request(upload_url, urllib.urlencode(params))
        #resp = urllib2.urlopen(req)
        #result = urlfetch.fetch(url=upload_url,
        #        payload=encd,
        #        method=urlfetch.POST)


class RandomPost(webapp2.RequestHandler):
    def get(self):

        # get random quote
        max_qu = db.GqlQuery('SELECT rand_int FROM Quote ORDER BY rand_int DESC LIMIT 1').get().rand_int
        rand_int = random.randint(1,max_qu)
        rand_qu = db.GqlQuery('SELECT * FROM Quote WHERE rand_int=%s' % rand_int).get()
        quote = rand_qu.quote
        author = rand_qu.author

        #logging.error(max_qu)
        #logging.error(rand_qu)
        #logging.error(quote)
        #logging.error(author)

        # get random background
        max_bg = db.GqlQuery('SELECT rand_int FROM BackgroundImage ORDER BY rand_int DESC LIMIT 1').get().rand_int
        rand_int = random.randint(1,max_bg)
        bg_url = db.GqlQuery('SELECT * FROM BackgroundImage WHERE rand_int=%s' % rand_int).get().url

        # overlay text
        img_out = addText(quote, author, bg_url)
        #img_out = '01'

        # save in datastore / blobstore
        # upload_url = blobstore.create_upload_url('/upload')
        p = Post(
                image=img_out,
                author=author,
                quote=quote
                )
        p.put()

        datHash = 'thisIsOurHashAndShit'
        channel.send_message(datHash,json.dumps({'key':str(p.key())}))

        self.redirect('/')

class Upload(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('img')
        if not upload_files:
            logging.error('HEREEEEEEEEEEEEEEEEEE')
            upload_files = self.request.get('img')
        blob_info = upload_files[0]

        logging.error('blob info: %s' % blob_info)
        logging.error('upload files: %s' % upload_files)



        image = blob_info.key()
        p = Post(
                image=images.get_serving_url(image),
                author=self.request.get('author'),
                quote=self.request.get('quote')
                )
        p.put()
        self.response.write('THERE')
        self.redirect('/')


class QuoteAdderAdmin(webapp2.RequestHandler):

    def get(self):
        author = self.request.get('author')
        quote = self.request.get('quote')
        template_values = {"author": author, "quote": quote}
        template = JINJA_ENVIRONMENT.get_template('admin_quote.html')
        self.response.write(template.render(template_values))

    def post(self):
        author = self.request.get('author')
        quote = self.request.get('quote')

        new_quote = Quote(author=author,quote=quote)
        new_quote.put()

        self.redirect('/quote?author=%s&quote=%s' % (author,quote))

class ViewHandler(webapp2.RequestHandler):
    def get(self):
        share = self.request.get('share')
        key = self.request.get('key')
        post = db.get(key)
        if not share:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(post.image)
        else:
            template_values = {
                    "upload_url": '/post',
                    "key": key,
                    }
            template = JINJA_ENVIRONMENT.get_template('post.html')
            self.response.write(template.render(template_values))


class MainPage(webapp2.RequestHandler):

    def get(self):
        limit = 4
        keys_qry = db.GqlQuery('SELECT __key__ FROM Post ORDER BY created DESC LIMIT %s' % (limit)).fetch(limit)

        datHash = 'thisIsOurHashAndShit'
        token = channel.create_channel(datHash)

        template_values = {
                "token": token,
                "upload_url": '/post',
                "keys": keys_qry
                }
        template = JINJA_ENVIRONMENT.get_template('base.html')
        self.response.write(template.render(template_values))



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/upload', Upload),
    ('/Update', Update),
    ('/quote', QuoteAdderAdmin),
    ('/post', UserPost),
    ('/view', ViewHandler),
    ('/random', RandomPost)
], debug=True)
