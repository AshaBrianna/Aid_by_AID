import jinja2
import logging
import os
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users

#college model

class Student(ndb.Model):
    home_location = ndb.StringProperty(required = True)
    budget = ndb.IntegerProperty(required = False, default = 0)
    prospective_colleges = ndb.StringProperty(required = False)
    grants = ndb.IntegerProperty(required = False, default = 0)
    email = ndb.StringProperty(required = True)

class College(ndb.Model):
    college_name = ndb.StringProperty(required = True)
    tuition = ndb.IntegerProperty(required = False, default = 0)
    housing = ndb.IntegerProperty(required = False, default = 0)
    food = ndb.IntegerProperty(required = False, default = 0)
    books = ndb.IntegerProperty(required = False, default = 0)
    student = ndb.KeyProperty(Student)

class CreateProfile(webapp2.RequestHandler):

    def get(self):

        template = jinja_env.get_template('templates/StudentProfile.html')
        self.response.write(template.render())

class AddCollegeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/AddCollege.html')
        self.response.write(template.render())

    def post(self):
        current_user = users.get_current_user()
        student_key = Student.query().filter(Student.email == current_user.email()).get().key
        College(
            college_name = self.request.get("college_name"),
            tuition = int(self.request.get("tuition")),
            housing = int(self.request.get("housing")),
            food = int(self.request.get("food")),
            books = int(self.request.get("books")),
            student = student_key,
        ).put()

        self.redirect("/", True)

#accesses the spreadsheet for now
class CollegeSelectorHandler(webapp2.RequestHandler):
    def get(self):
        #check if logged in user has a student in datastore, if yes get their key,
        #if not, add a new student to datastore
        current_user = users.get_current_user()
        student = Student.query().filter(Student.email == current_user.email()).get()
        if student == None:
            #TODO if a user does not have a student instance, redirect them to profile creation page
            student_key = Student(home_location = "home", email = current_user.email()).put()
        else:
            student_key = student.key
        college_list = College.query().filter(College.student==student_key)
        template = jinja_env.get_template('templates/MainPage.html')

        template_vars ={
            "college" : college_list,
            "logout_url": users.create_logout_url('/')

        }
        self.response.write(template.render(template_vars))

class PopulateDataBase(webapp2.RequestHandler):
    def get(self):
        uc_berkley = College(college_name = "UC Berkley", tuition = 14254, housing = 17220, food = 1644, books = 870, student = student_key).put()
        redirect

class PreCodedCollegeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/SelectCollege.html')
        college_list = College.query().filter(College.student==student_key)

        template_vars ={
        "college" : college_list,
        "logout_url": users.create_logout_url('/')

        }

        self.response.write(template.render(template_vars))



jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)
app = webapp2.WSGIApplication([
    ('/', CollegeSelectorHandler),
    ('/add_college', AddCollegeHandler),
    ('/AddStudent', CreateProfile),
     # ('/', ComparisonHandler),


], debug=True)
