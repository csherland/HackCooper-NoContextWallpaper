import webapp2
import json
import jinja2
import os
import datetime

from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from google.appengine.api import images

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class BackgroundImage(db.Model):
    url = db.StringProperty(multiline=True)

class Font(db.Model):
    font = db.StringProperty()

class Post(db.Model):
    image = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    quote = db.StringProperty()
    font = db.ReferenceProperty(Font)
    background = db.ReferenceProperty(BackgroundImage)
    byline = db.StringProperty()

class Quote(db.Model):
    quote = db.StringProperty(multiline=True)
    author = db.StringProperty(multiline=True)

class Upload(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        post = Post()
        post.image = self.request.get('image')
        post.quote = self.request.get('quote')
        post.font = self.request.get('font')
        post.background = self.request.get('background')

        upload_files = self.get_uploads('img')  # 'file' is file upload field in the form
        if upload_files:
            blob_info = upload_files[0]
            image = blob_info.key() #self.request.get('img')
            post.image = images.get_serving_url(image)
        post.put()
        self.redirect('/')

class Update(webapp2.RequestHandler):

    def get(self):
        posts = self.request.get('posts')

class MainPage(webapp2.RequestHandler):

    def get(self):

        template_values = {
                }
        template = JINJA_ENVIRONMENT.get_template('base.html')
        self.response.write(template.render(template_values))

class QuoteAdderAdmin(webapp2.RequestHandler):

    def get(self):
        quotes_qry = Quote.all()
        template_values = {"quotes": quotes_qry}
        template = JINJA_ENVIRONMENT.get_template('admin_quote.html')
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/Upload', Upload),
    ('/Update', Update),
    ('/admin/quote', QuoteAdderAdmin),
], debug=True)
