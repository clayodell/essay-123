from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os

class IndexHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), '../views' , 'index.html')
#        self.response.out.write(path)
        self.response.out.write(
                              template.render(path, {
                              "title" : "Essay"
                              })
        )

class RegisterHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), '../views' , 'register.html')
        self.response.out.write(
                              template.render(path, {
                              "title" : "Essay"
                              })
        )

class TopicHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), '../views' , 'add-topic.html')
        self.response.out.write(
                              template.render(path, {
                              "title" : "Essay"
                              })
        )