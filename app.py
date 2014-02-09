import webapp2
import json
import jinja2
import os
import datetime
import urllib2

from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from google.appengine.api import images

from nocontext.addText import addText

import random

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
    image = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    quote = db.StringProperty()
    #font = db.ReferenceProperty(Font)
    #background = db.ReferenceProperty(BackgroundImage)
    author = db.StringProperty()

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

class MainPage(webapp2.RequestHandler):

    def get(self):

        template_values = {
                "upload_url": '/post'
                }
        template = JINJA_ENVIRONMENT.get_template('base.html')
        self.response.write(template.render(template_values))

class UserPost(blobstore_handlers.BlobstoreUploadHandler):
#class Upload(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        # TODO: random quote if random button hit, otherwise do user quote
        author = self.request.get('author')
        quote = self.request.get('quote')

        # get random background
        max_bg = db.GqlQuery('SELECT rand_int FROM BackgroundImage ORDER BY rand_int DESC LIMIT 1').get().rand_int
        bg_url = db.GqlQuery('SELECT * FROM BackgroundImage WHERE rand_int=%s' % max_bg).get().url

        # overlay text
        img_out = addText(quote, author, bg_url)

        # save in datastore / blobstore
        upload_url = blobstore.create_upload_url('/upload')

        params = {"author":author,
                "quote":quote,
                "img":img_out
                }

        req = urllib2.Request(upload_url, urllib.urlencode(params))

#        post.image = images.get_serving_url(image)
#        p = Post(
#                image=images.get_serving_url(image)
#        post.put()

class Upload(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('img')
        blob_info = upload_files[0]

        image = blob_info.key()
        p = Post(
                image=images.get_serving_url(image),
                author=self.request.get('author'),
                quote=self.request.get('quote')
                )
        p.put()


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



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/upload', Upload),
    ('/Update', Update),
    ('/quote', QuoteAdderAdmin),
    ('/post', UserPost),
], debug=True)
