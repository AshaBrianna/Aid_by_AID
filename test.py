import unirest
import ssl
import json



def Flights(Student, College):
    flights_response = unirest.get("https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsedates/v1.0/US/USD/en-US/SFO-sky/LAX-sky/2019-09-01?inboundpartialdate=2019-12-01",
      headers={
        "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "3b06a903famshe856af999ade62ap14f722jsnfb9f1e392c75"
      },
      params={
        "inboundDate": "2019-09-10",
        "cabinClass": "business",
        "children": 0,
        "infants": 0,
        "country": "US",
        "currency": "USD",
        "locale": "en-US",
        "originPlace": Student.home_location,
        "destinationPlace": College.college_location,
        "outboundDate": "2019-09-01",
        "adults": 1
      }
    )

    flights_dictionary = json.loads(flights_response.raw_body)
    print 'flights_dictionary', flights_dictionary
    print flights_dictionary['Quotes'][0]["MinPrice"]
    # template_vars = {
    #     'prices': flights_dictionary[Quotes][MinPrice],
    # }

    # template = jinja_env.get_template('templates/StudentProfile.html')
    # self.response.write(template.render(template_vars))

Flights(['params'][originPlace]JFK, ['params']"LAX")

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
    college_location = ndb.StringProperty(required = False)
    student = ndb.KeyProperty(Student)
