import jinja2
import logging
import os
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users


# Step 2: Set up Jinja Environment
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
)

#college model
class College(ndb.Model):
    college_name = ndb.StringProperty(required = True)
    tuition = ndb.IntegerProperty(required = True)
    housing = ndb.IntegerProperty(required = True)
    food = ndb.IntegerProperty(required = True)
    books = ndb.IntegerProperty(required = True)
class UserColleges(ndb.Model):
    user_name = ndb.StringProperty(required = True)
    user_tuition = ndb.IntegerProperty(required = True)
    user_housing = ndb.IntegerProperty(required = True)
    user_food = ndb.IntegerProperty(required = True)
    user_books = ndb.IntegerProperty(required = True)
class UserInfo(ndb.Model):
    user_budget = ndb.IntegerProperty(requr)

#creating database
class PopulateDataBase(webapp2.RequestHandler):
    def get(self):
        boston_universiy = College(name = "Boston University", tuition = 54720, housing = 10680, food = 5480, books = 1000).put()
        boston_universiy = College(name = "Boston University", tuition = 54720, housing = 10680, food = 5480, books = 1000).put()


        self.redirect("/", True)

#Page for adding colleges to the user's "college shopping list"
class CollegeSelectorHandler(webapp2.RequestHandler):

    def get(self):
        college_list = College.query().fetch()
        template = jinja_env.get_template('MainPage.html')

        template_vars ={
            "college": college_list,
            # "college_name": self.request.get("college_name"),
            # "housing": self.request.get("housing"),
            # "travel": self.request.get("travel"),
            # "tuition": self.request.get("tuition"),
            # "food": self.request.get("food"),
            # "books": self.request.get("books"),
        }

        self.response.write(template.render(template_vars))

class ComparisonHandler(webapp2.RequestHandler):
     def get(self):
        template = jinja_env.get_template('MainPage.html')
        self.response.write(template.render())



jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)
app = webapp2.WSGIApplication([
    ('/', CollegeSelectorHandler),
    ('/populateDatabase', PopulateDataBase),
     ('/Compare', ComparisonHandler),


], debug=True)
