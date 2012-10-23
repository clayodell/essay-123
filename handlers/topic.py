from google.appengine.ext import webapp
from google.appengine.ext import db
from models.Models import Topic
from google.appengine.api import users
from google.appengine.ext.webapp import template
import os
import json
from datetime import datetime
import library.helpers
from handlers import user

class CreateTopic(webapp.RequestHandler):
    def get(self):
        currentUser = user.getUserbyEmail(user.getLoggedInUser())
        if(not currentUser):
            self.error(403)
            self.response.out.write("not logged in")
        else:
            userMeta = json.loads(currentUser.metadata)
            if(not userMeta['profile_completed']):
                self.redirect("/complete_profile")
            else:
                path = os.path.join(os.path.dirname(__file__), '../views' , 'add-topic.html')
                self.response.out.write(
                  template.render(path,locals())
                  )

class DoAddTopic(webapp.RequestHandler):
    def post(self):
        currentUser = user.getUserbyEmail(user.getLoggedInUser())
        if(not currentUser):
            self.error(403)
            self.response.out.write("not logged in")
        else :
            userMeta = json.loads(currentUser.metadata)
            if(not userMeta['profile_completed']):
                self.response.out.write("profile not completed")
            else:
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
        logoutUrl = users.create_logout_url(self.request.uri)
        topics = Topic.all()
        topics.filter('access_type = ', 1)
        topics.filter('is_deleted = ', False)
        topicsArray = []
        currentUser = user.getUserbyEmail(user.getLoggedInUser())
        for topic in topics:
            topicDict = {}
            topicDict['id'] = topic.key()
            topicDict['title'] = topic.title
            topicDict['added_duration'] = library.helpers.getTimeInDaysMinutesSeconds(library.helpers.getSecondsFromNow(topic.created))
            topicDict['keywords'] = json.loads(topic.tags)
            topicDict['owner'] = topic.owner.nickname
            topicsArray.append(topicDict)
            
            if(currentUser and topic.owner.email == currentUser.email):
                topicDict['is_owner'] = True
                
        path = os.path.join(os.path.dirname(__file__), '../views' , 'topics.html')
        self.response.out.write(
              template.render(path,locals())
        )

class editTopic(webapp.RequestHandler):
    def get(self):
        try:
            key = self.request.get("t")
            if(key):
                topicKey = db.Key(key)
                topic = Topic.get(topicKey)
                tags = json.loads(topic.tags)
                currentUser = user.getLoggedInUser()
                if(not currentUser):
                    print "not logged in"
                    self.error(403)
                elif (topic.owner.email == currentUser):
                    path = os.path.join(os.path.dirname(__file__), '../views' , 'edit-topic.html')
                    self.response.out.write(
                        template.render(path,locals())
                    )
                else:
                    print "Not the owner of the topic"
                    self.error(403)
            else:
                self.error(500)
        except Exception:
            print Exception.message

class doEditTopic(webapp.RequestHandler):
    def post(self):
        try:
            key = self.request.get("t")
            if(key):
                currentUser = user.getUserbyEmail(user.getLoggedInUser())
                if(not currentUser):
                    print "not logged in"
                    self.error(403)
                else:
                    topicKey = db.Key(key)
                    topic = Topic.get(topicKey)
                    if(not topic):
                        print "Invalid key"
                        self.error(500)
                    else:
                        modifierArray = []
                        if (topic.owner.email == currentUser.email):
                            tags = (self.request.get_all("tags[]"))
                            tags = json.dumps(tags)
                            title = self.request.get('title')
                            descrtiption = self.request.get("description")
                            accessType = int(self.request.get("access_type"))
                            topic.title = title
                            topic.description = descrtiption
                            topic.access_type = accessType
                            topic.tags = tags
                            topicHistory = topic.history
                            if(topicHistory):
                                topicHistoryArray = json.loads(topic.history)
                                for myTopic in topicHistoryArray:
                                    modifierArray.append(myTopic)
                            historyDict = {}
                            historyDict['modifier'] = user.getLoggedInUser()
                            time = datetime.now()
                            historyDict['modified'] = time.strftime("%b %d %Y %H:%M:%S")
                            modifierArray.append(historyDict)
                            historyJson = json.dumps(modifierArray)
                            topic.history =  historyJson
                            topic.put()  
                            self.redirect("/topics")
                        else:
                            print "Not the owner of the topic"
                            self.error(403)
            else:
                self.error(500)
        except Exception:
            print Exception.message
            
class DoDeleteTopic(webapp.RequestHandler):
    def get(self):
        currentUser = user.getUserbyEmail(user.getLoggedInUser())
        if(not currentUser):
            self.response.out.write("not logged in")
        else:
            key = self.request.get("t")
            if(not key):
                self.response.out.write("Arguments missing")
            else:
                topicKey = db.Key(key)    
                topic = Topic.get(topicKey)
                if(not topic):
                    self.response.out.write("Invalid key")
                else:
                    if (not topic.owner.email == currentUser.email):
                        self.response.out.write("You do not have the rights to delete this topic")
                    else:
                        topic.is_deleted = True
                        metaData = {}
                        time = datetime.now()
                        metaData['delete_date'] = time.strftime("%b %d %Y %H:%M:%S")
                        metaData['deleted_by'] = currentUser.nickname
                        topic.deleteMetaData = json.dumps(metaData)
                        topic.put()
                        self.response.out.write('success')