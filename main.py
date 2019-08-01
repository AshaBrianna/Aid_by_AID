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
    other = ndb.IntegerProperty(required = False, default = 0)
    student = ndb.KeyProperty(Student)
    college_key = ndb.KeyProperty(repeated = True)
    travel = ndb.IntegerProperty(required = False)
    college_location = ndb.StringProperty(required = False)

class PreLoadedCollege(ndb.Model):
    college_name = ndb.StringProperty(required = True)
    tuition = ndb.IntegerProperty(required = False, default = 0)
    housing = ndb.IntegerProperty(required = False, default = 0)
    food = ndb.IntegerProperty(required = False, default = 0)
    books = ndb.IntegerProperty(required = False, default = 0)
    other = ndb.IntegerProperty(required = False, default = 0)
    travel = ndb.IntegerProperty(required = False)
    college_location = ndb.StringProperty(required = False)
    student = ndb.KeyProperty(Student)


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
        self.redirect("/", True)

#accesses the spreadsheet for now
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
            "logout_url": users.create_logout_url('/'),
            "budget": student.budget,
        }
        print(College.travel)
        self.response.write(template.render(template_vars))

class PopulateDataBase(webapp2.RequestHandler):
    def get(self):
        uc_berkley = PreLoadedCollege(college_name = "UC Berkeley", tuition = 14254, housing = 17220, food = 1644, books = 870, other = 0, college_location = "OAK").put()
        uc_riverside = PreLoadedCollege(college_name = "UC Riverside", tuition = 15602, housing = 17475, food = 6099, books = 1400, other = 0, college_location = "RAL").put()
        uc_davis = PreLoadedCollege(college_name = "UC Davis", tuition = 14490, housing = 15863, food = 0, books = 1159, other = 0, college_location = "SJC").put()
        uc_la = PreLoadedCollege(college_name = "UC Los Angeles", tuition = 13239, housing = 16625, food = 0, books = 1464, other = 0, college_location = "SJC").put()
        uc_sc = PreLoadedCollege(college_name = "UC Santa Cruz", tuition = 13989, housing = 16950, food = 0, books = 1086, other = 0).put()
        uc_sd= PreLoadedCollege(college_name = "UC San Diego", tuition = 14451, housing = 14295, food = 0, books = 1128, other = 0).put()
        uc_irvine= PreLoadedCollege(college_name = "UC Irvine", tuition = 15797, housing = 19744, food = 0, books = 0, other = 0).put()
        uc_merced= PreLoadedCollege(college_name = "UC Merced", tuition = 13538, housing = 17046, food = 0, books = 1016, other = 0).put()
        uc_sb= PreLoadedCollege(college_name = "UC Santa Barbara", tuition = 12570, housing = 15111, food = 0, books = 1185, other = 1875).put()
        stanford = PreLoadedCollege(college_name = "Stanford University", tuition = 52857, housing = 16433, food = 0, books = 1245, other = 1905).put()
        st_marys = PreLoadedCollege(college_name = "St. Mary's College", tuition = 32140, housing = 10720, food = 0, books = 1300, other = 0).put()
        occidental = PreLoadedCollege(college_name = "Occidental College", tuition = 55980, housing = 9124, food = 6910, books = 1500, other = 600).put()
        pomona = PreLoadedCollege(college_name = "Pomona University", tuition = 54380, housing = 17218, food = 0, books = 1500, other = 382).put()
        santaclara= PreLoadedCollege(college_name = "Santa Clara University", tuition = 52998, housing = 15507, food = 0, books = 1971, other = 636).put()
        usc = PreLoadedCollege(college_name = "USC", tuition = 57256, housing = 15916, food = 0, books = 1200, other = 939).put()
        calpoly= PreLoadedCollege(college_name = "Cal Poly SLO", tuition = 9942, housing = 14208, food = 0, books = 2000, other = 0).put()
        caltech = PreLoadedCollege(college_name = "Cal Tech", tuition = 52506, housing = 9615, food = 7029, books = 1428, other = 2094).put()
        pepperdine = PreLoadedCollege(college_name = "Pepperdine", tuition = 55640, housing = 15670, food = 0, books = 1250, other = 0).put()
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
                student_airport = Student.query().filter(Student.email == current_user.email()).get().home_location
                logging.info(student_airport)
                full_url= "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/USD/en-US/" + str(college.college_location) + '/' + str(student_airport) + "/2019-09-01?inboundpartialdate=2019-12-01/"
                flights_response = urlfetch.fetch(
                full_url,
                  headers={
                    "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
                    "X-RapidAPI-Key": "3b06a903famshe856af999ade62ap14f722jsnfb9f1e392c75"
                  },
                )
                flights_dictionary = json.loads(flights_response.content)
                College(
                    college_name = college.college_name,
                    tuition = college.tuition,
                    housing = college.housing,
                    food = college.food,
                    books = college.books,
                    student = student_key,
                    other = college.other,
                    travel = int(flights_dictionary["Quotes"][0]["MinPrice"]),
                    college_location = college.college_location,
                ).put()

        self.redirect('/', True)

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)

app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/add_college', AddCollegeHandler),
    ('/AddStudent', CreateProfile),
    ('/populateDatabase', PopulateDataBase),
    ('/preloaded_colleges', PreCodedCollegeHandler),
     # ('/', ComparisonHandler),
], debug=True)
