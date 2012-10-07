from google.appengine.ext import webapp
from models.Models import Topic
from google.appengine.ext.webapp import template
from datetime import datetime
import os
import json
from library.helpers import Helpers

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
        mytopic.owner = "Faizan"
        mytopic.is_deleted = False
        mytopic.put()        
        self.redirect("/topics")
        
        
class viewPublicTopics(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), '../views' , 'topics.html')
        topics = Topic.all()
        topics.filter('access_type = ',1)
        topics.filter('is_deleted = ',False)
        d1 = datetime.now();
        d2 = topics[0].created
        d3 = d1-d2
        d4 = d3.seconds
        obj = Helpers()
        self.response.out.write(obj.getTimeInDaysMinutesSeconds(86400))
#        self.response.out.write(
#              template.render(path, {
#              "topics" : topics,
#              "title" : "Essay",
#              })
#        )
