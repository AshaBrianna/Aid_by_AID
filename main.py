import jinja2
import logging
import os
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users

class Student(ndb.Model):
    home_location = ndb.StringProperty(required = True)
    budget = ndb.IntegerProperty(required = False, default = 0)
    prospective_colleges = ndb.StringProperty(required = False, default = 0)
    grants = ndb.IntegerProperty(required = False, default = 0)
    emails = ndb.StringProperty(required = True, default = 0)
     
#college model
class College(ndb.Model):
    college_name = ndb.StringProperty(required = True)
    tuition = ndb.IntegerProperty(required = False, default = 0)
    housing = ndb.IntegerProperty(required = False, default = 0)
    food = ndb.IntegerProperty(required = False, default = 0)
    books = ndb.IntegerProperty(required = False, default = 0)





class AddCollegeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/AddCollege.html')
        self.response.write(template.render())

    def post(self):
        College(college_name = self.request.get("college_name"), tuition = int(self.request.get("tuition")), housing = int(self.request.get("housing")), food = int(self.request.get("food")), books = int(self.request.get("books"))).put()

        self.redirect("/", True)
#Page for adding colleges to the user's "college shopping list"
# class BudgetHandler(webapp2.RequestHandler):
#     def get(self):
#         template = jinja_env.get_template('AddBudget.html')

#accesses the spreadsheet for now
class CollegeSelectorHandler(webapp2.RequestHandler):
    def get(self):
        college_list = College.query().fetch()
        template = jinja_env.get_template('templates/MainPage.html')

        template_vars ={
            "college" : college_list,

        }
        self.response.write(template.render(template_vars))

class BudgetHandler(webapp2.RequestHandler):

    def get(self):

        template = jinja_env.get_template('AddBudget.html')
        self.response.write(template.render())

#
# class ComparisonHandler(webapp2.RequestHandler):
#      def get(self):
#         template = jinja_env.get_template('Comparison.html')
#         self.response.write(template.render())



jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)
app = webapp2.WSGIApplication([
    ('/', CollegeSelectorHandler),
    ('/add_college', AddCollegeHandler),
    ('/addBudget', BudgetHandler),
     # ('/', ComparisonHandler),


], debug=True)
