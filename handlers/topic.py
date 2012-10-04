from google.appengine.ext import webapp
from models.Models import Topic

class addTopic(webapp.RequestHandler):
    def post(self):
        title = self.request.get("title")
        descrtiption = self.request.get("description")
        accessType = int(self.request.get("access_type"))
        mytopic = Topic()
        mytopic.title = title
        mytopic.description = descrtiption
        mytopic.access_type = accessType
        mytopic.owner = "sh.faizan.ali@hotmail.com"
        mytopic.is_deleted = False
        mytopic.put()
        self.redirect("/topics")
        
