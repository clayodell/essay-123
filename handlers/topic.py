from google.appengine.ext import webapp
from models.Models import Topic
from google.appengine.ext.webapp import template
import os
import json

class addTopic(webapp.RequestHandler):
    def post(self):
        tags = (self.request.get_all("tags[]"))
        tags = json.dumps(tags)
        title = self.request.get("title")
        descrtiption = self.request.get("description")
        accessType = int(self.request.get("access_type"))
        mytopic = Topic()
        mytopic.title = title
        mytopic.description = descrtiption
        mytopic.access_type = accessType
        mytopic.tags = tags
        mytopic.owner = "sh.faizan.ali@hotmail.com"
        mytopic.is_deleted = False
        mytopic.put()        
        self.redirect("/topics")
        
        
class viewTopics(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), '../views' , 'topics.html')
        topics = Topic.all()
          
        self.response.out.write(
                              template.render(path, {
                              "topics" : topics,
                              "title" : "Essay",
                              })
        )