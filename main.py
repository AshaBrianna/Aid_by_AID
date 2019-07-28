import webapp2
import logging
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import users


#
# app = webapp2.WSGIApplication([
#     ('/', Page)
# ], debug=True)
