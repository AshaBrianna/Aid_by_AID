import jinja2
import logging
import os
import webapp2
import time


from google.appengine.ext import ndb
from google.appengine.api import users

#college model

class Student(ndb.Model):
    home_location = ndb.StringProperty(required = True)
    student_name = ndb.StringProperty(required = True)
    budget = ndb.IntegerProperty(required = False, default = 0)
    grants = ndb.IntegerProperty(required = False, default = 0)
    email = ndb.StringProperty(required = True)

class College(ndb.Model):
    college_name = ndb.StringProperty(required = True)
    tuition = ndb.IntegerProperty(required = False, default = 0)
    housing = ndb.IntegerProperty(required = False, default = 0)
    food = ndb.IntegerProperty(required = False, default = 0)
    books = ndb.IntegerProperty(required = False, default = 0)
    student = ndb.KeyProperty(Student)

class PreLoadedCollege(ndb.Model):
    college_name = ndb.StringProperty(required = True)
    tuition = ndb.IntegerProperty(required = False, default = 0)
    housing = ndb.IntegerProperty(required = False, default = 0)
    food = ndb.IntegerProperty(required = False, default = 0)
    books = ndb.IntegerProperty(required = False, default = 0)

class CreateProfile(webapp2.RequestHandler):

    def get(self):

        template = jinja_env.get_template('templates/StudentProfile.html')
        self.response.write(template.render())
    def post(self):
        current_user = users.get_current_user()
        student_key = Student(student_name = self.request.get("student_name"),
                home_location = self.request.get("home_location"),
                budget = int(self.request.get("budget")),
                grants = int(self.request.get("grants")),
                email = current_user.email()
                ).put()
        #time.sleep(.3)

        self.redirect("/?student_key=%s" % student_key.urlsafe(), True)

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

        urlsafe_key = self.request.get("student_key")
        if urlsafe_key != "":
            key = ndb.Key(urlsafe = urlsafe_key)
            student = key.get()
        else:
            current_user = users.get_current_user()
            student = Student.query().filter(Student.email == current_user.email()).get()

        if student is None:
            #TODO if a user does not have a student instance, redirect them to profile creation page
            self.redirect("/AddStudent", True)
            return
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
        uc_berkley = PreLoadedCollege(college_name = "UC Berkley", tuition = 14254, housing = 17220, food = 1644, books = 870).put()
        uc_riverside = PreLoadedCollege(college_name = "UC Riverside", tuition = 15602, housing = 17475, food = 6099, books = 1400).put()
        uc_davis = PreLoadedCollege(college_name = "UC Davis", tuition = 14490, housing = 15863, food = 0, books = 1159).put()
        self.redirect('/', True)

class PreCodedCollegeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/SelectCollege.html')
        college_list = PreLoadedCollege.query().fetch()
        template_vars = {
        "college" : college_list,
        "logout_url": users.create_logout_url('/'),
        }

        self.response.write(template.render(template_vars))

    def post(self):
        college_list = PreLoadedCollege.query().fetch()
        for college in college_list:
            selected = self.request.get(college.college_name)
            if selected:
                current_user = users.get_current_user()
                student_key = Student.query().filter(Student.email == current_user.email()).get().key
                College(
                    college_name = college.college_name,
                    tuition = college.tuition,
                    housing = college.housing,
                    food = college.food,
                    books = college.books,
                    student = student_key,
                ).put()

        self.redirect('/', True)


jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)
app = webapp2.WSGIApplication([
    ('/', CollegeSelectorHandler),
    ('/add_college', AddCollegeHandler),
    ('/AddStudent', CreateProfile),
    ('/populateDatabase', PopulateDataBase),
    ('/college_list', PreCodedCollegeHandler),
     # ('/', ComparisonHandler),


], debug=True)
