import webapp2
import logging
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import users


# Step 2: Set up Jinja Environment
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
)

class AddCollege (webapp2.RequestHandler):
        def get(self):
            template = jinja_env.get_template('AddCollege.html')
            self.response.write(template.render())

        def post(self):
            template_vars = {
                "college_name": self.request.get("college_name"),
                "housing": self.request.get("housing"),
                "travel": self.request.get("travel"),
                "tuition": self.request.get("tuition"),
            }
            template = jinja_env.get_template('MainPage.html')
            self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', AddCollege),
], debug=True)
