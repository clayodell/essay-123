from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from models.Models import Essay,Topic,Rating
from handlers import user
import os
import json
#import pprint
class NewEssay(webapp.RequestHandler):
    def get(self):
        key = self.request.get("t")
        topic = Topic.get(key)
        if not topic:
            print "No Topic with this id found"
            self.error(500)
        else:
            topic_id = topic.key()
            current_user = users.get_current_user()
            if not current_user:
                self.redirect('/login')
            else:
                path = os.path.join(os.path.dirname(__file__), '../views' , 'new-essay.html')
                self.response.out.write(
                    template.render(path,locals())
                )
            
class CreateEssay(webapp.RequestHandler):
    def post(self):
        key = self.request.get("t")
        topic = Topic.get(key)
        currentUser = user.getUserbyId(user.getLoggedInUser())
        if not currentUser:
            self.redirect('/login')
        else:
            myEssay = Essay()
            myEssay.essay_text = self.request.get("essay-text")
            myEssay.parent_topic = topic.key()
            myEssay.owner = currentUser.key()
            myEssay.put()
            self.redirect('/essays?t='+key)

class ShowEssays(webapp.RequestHandler):
    def get(self):
        key = self.request.get("t")
        topic = Topic.get(key)
        if not topic:
            print "No Topic with this id found"
            self.error(500)
        else:
            topic_id = topic.key()
#            currentUser = user.getUserbyId(user.getLoggedInUser())
            path = os.path.join(os.path.dirname(__file__), '../views' , 'essays.html')
            self.response.out.write(
                    template.render(path,locals())
                )
            
class SaveRatings(webapp.RequestHandler):
    def post(self):
        ratingPoints = self.request.get('rate')
        essayID = self.request.get('idBox')
        currentUser = user.getUserbyId(user.getLoggedInUser())
        responseDict = {}
        if(not currentUser):
            responseDict['code'] = -1
            responseDict['message'] = "You must be logged in to rate the essay";
            self.response.out.write(json.dumps(responseDict))
        else:
            objEssay = Essay.get(essayID)
            objRating = Rating()
            objRating.rated_by = currentUser.key()
            objRating.essay = objEssay.key()
            objRating.rating = ratingPoints 
            objRating.put()
            responseDict['code'] = 0
            responseDict['message'] = "Your rating has been posted"
            self.response.out.write(json.dumps(responseDict))

class AddComment(webapp.RequestHandler):
    def post(self):
        currentUser = user.getUserbyId(user.getLoggedInUser())
        responseDict = {}
        if(not currentUser):
            responseDict['code'] = -1
            responseDict['message'] = "You must be logged in to rate the essay";
            self.response.out.write(json.dumps(responseDict))
        else:
            comment = self.request.get('comment')
            essayID = self.request.get('essay_id')
            userKey = currentUser.key()
            objEssay = Essay.get(essayID)
            if not objEssay:
                responseDict['code'] = -2
                responseDict['message'] = "No Essay with this Id found";
                self.response.out.write(json.dumps(responseDict))
            else:
                
                