import jinja2
import logging
import os
import webapp2
import json
import time
import urllib


from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import urlfetch

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)



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
    college_location = ndb.StringProperty(required = False)
    student = ndb.KeyProperty(Student)
    college_key = ndb.KeyProperty(repeated = True)
    travel = ndb.IntegerProperty(required = True)
    #college_location = ndb.StringProperty(required = True)

class PreLoadedCollege(ndb.Model):
    college_name = ndb.StringProperty(required = True)
    tuition = ndb.IntegerProperty(required = False, default = 0)
    housing = ndb.IntegerProperty(required = False, default = 0)
    food = ndb.IntegerProperty(required = False, default = 0)
    books = ndb.IntegerProperty(required = False, default = 0)
    # college_location = ndb.StringProperty(required = False)


class CreateProfile(webapp2.RequestHandler):

    def get(self):

        template = jinja_env.get_template('templates/StudentProfile.html')
        self.response.write(template.render())
    def post(self):
        current_user = users.get_current_user()
        student_key = Student(student_name = self.request.get("student_name"),
                home_location = self.request.get("home_location"),
                # home_location = self.request.get("home_location"),
                budget = int(self.request.get("budget")),
                grants = int(self.request.get("grants")),
                email = current_user.email()
                ).put()
        student_budget = self.request.get("budget")

        self.redirect("/?student_key=%s&student_budget=%s" % (student_key.urlsafe(), student_budget), True)

class AddCollegeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/AddCollege.html')
        self.response.write(template.render())

    def post(self):
        logging.info('starts post')
        fly_to = self.request.get("college_location")
        fly_from = self.request.get("home_location")
        current_user = users.get_current_user()
        student_key = Student.query().filter(Student.email == current_user.email()).get().key
        student = Student.query().filter(Student.email == current_user.email()).get()
        if student == None:
            self.redirect('/', True)
            return
        # college_location = 'college'
        # home_location = 'home'
        # current_user = users.get_current_user()
        # # TODO: Add case for admin login
        full_url= "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/USD/en-US/" + str(fly_to) + '/' + str(fly_from) + "/2019-09-01?inboundpartialdate=2019-12-01/"
        flights_response = urlfetch.fetch(
        full_url,
          headers={
            "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
            "X-RapidAPI-Key": "3b06a903famshe856af999ade62ap14f722jsnfb9f1e392c75"
          },
        )
# # student_key.get().home_location,student_key.get().college_location,
#
        flights_dictionary = json.loads(flights_response.content)
        College(
            college_name = self.request.get("college_name"),
            college_location = self.request.get("college_location"),
            tuition = int(self.request.get("tuition")),
            housing = int(self.request.get("housing")),
            food = int(self.request.get("food")),
            books = int(self.request.get("books")),
            travel = int(flights_dictionary["Quotes"][0]["MinPrice"]),
            student = student_key,
            ).put()

class MainPageHandler(webapp2.RequestHandler):
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



app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/add_college', AddCollegeHandler),
    ('/AddStudent', CreateProfile),
    ('/populateDatabase', PopulateDataBase),
    ('/preloaded_colleges', PreCodedCollegeHandler),
     # ('/', ComparisonHandler),


], debug=True)
