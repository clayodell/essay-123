from google.appengine.ext import webapp
from models.Models import Topic
from google.appengine.ext.webapp import template
import os
import json
import library.helpers

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
        topics.filter('access_type = ', 1)
        topics.filter('is_deleted = ', False)
        topicsArray = []
        for topic in topics:
            topicDict = {}
            topicDict['id'] = topic.key().id()
            topicDict['title'] = topic.title
            topicDict['added_duration'] = library.helpers.getTimeInDaysMinutesSeconds(library.helpers.getSecondsFromNow(topic.created))
            topicDict['keywords'] = json.loads(topic.tags)
            topicDict['owner'] = topic.owner
            topicsArray.append(topicDict)

#        self.response.out.write(topicsArray)
        self.response.out.write(
              template.render(path,locals())
        )
