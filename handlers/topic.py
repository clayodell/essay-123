from google.appengine.ext import webapp
from google.appengine.ext import db
from models.Models import Topic
from google.appengine.ext.webapp import template
import os
import json
import library.helpers
from handlers import user


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
        owner = user.getUserbyEmail(user.getLoggedInUser())
        mytopic.owner = owner.key()
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
        self.response.out.write(topics)
        for topic in topics:
            topicDict = {}
            topicDict['id'] = topic.key()
            topicDict['title'] = topic.title
            topicDict['added_duration'] = library.helpers.getTimeInDaysMinutesSeconds(library.helpers.getSecondsFromNow(topic.created))
            topicDict['keywords'] = json.loads(topic.tags)
            topicDict['owner'] = topic.owner.nickname
            topicsArray.append(topicDict)
        self.response.out.write(
              template.render(path,locals())
        )

class editTopic(webapp.RequestHandler):
    def get(self):
        try:
            key = self.request.get("key")
            if(key):
                topicKey = db.Key(key)
                topic = Topic.get(topicKey)
                tags = json.loads(topic.tags)
                if (topic.owner.email == user.getLoggedInUser()):
                    path = os.path.join(os.path.dirname(__file__), '../views' , 'edit-topic.html')
                    self.response.out.write(
                        template.render(path,locals())
                    )
                else:
                    self.error(403)
            else:
                self.error(500)
        except Exception:
            print Exception.message

class doEditTopic(webapp.RequestHandler):
    def post(self):
        try:
            key = self.request.get("key")
            if(key):
                topicKey = db.Key(key)
                topic = Topic.get(topicKey)
                if (topic.owner.email == user.getLoggedInUser()):
                    tags = (self.request.get_all("tags[]"))
                    tags = json.dumps(tags)
                    title = self.request.get('title')
                    descrtiption = self.request.get("description")
                    accessType = int(self.request.get("access_type"))
                    topic.title = title
                    topic.description = descrtiption
                    topic.access_type = accessType
                    topic.tags = tags
                    topic.put()
                    self.redirect("/topics")
                else:
                    self.error(403)
            else:
                self.error(500)
                topic = Topic.get(topicKey)
        except Exception:
            print Exception.message
            