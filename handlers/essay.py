from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from models.Models import Essay,Topic
from library.constants import *
from library.helpers import *
from handlers import user
import os
import json
#import sys
from datetime import datetime
#import pprint
#############################################################################################################
#                           REQUEST HANDLER TO VIEW THE ESSAY PAGE 
#############################################################################################################
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

#############################################################################################################
#                           CREATE ESSAY REQUEST HANDLER
#############################################################################################################

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
            
            
##########################################################################################
#                 SREQUEST HANDLER TO VIEW THE ESSAYS
##########################################################################################

class ShowEssays(webapp.RequestHandler):
    def get(self):
        key = self.request.get("t")
        topic = Topic.get(key)
        if not topic:
            print "No Topic with this id found"
            self.error(500)
        else:
            curentUser = user.getUserbyId(user.getLoggedInUser())
            topic_id = topic.key()
            essaysArray = []
            for essay in topic.topic:
                essayDict = {}
                essayDict['essay_text'] = essay.essay_text
                essayDict['owner_name'] = essay.owner.nickname
                essayDict['owner_id'] = essay.owner.id
                essayDict['essay_key'] = essay.key()
                essayDict['created'] = getTimeInDaysMinutesSeconds(getSecondsFromNow(essay.created))
                if(essay.ratings):
                    essayDict['ratings'] = json.loads(essay.ratings)
                    essayDict['my_ratings'] = self.getMyRatings(essay.ratings, curentUser)
                    
                else:
                    essayDict['ratings'] ={'count':0,'aggregate_rating':0}
                    essayDict['my_ratings'] = 0
                if essay.comments:
                    essayDict['comments'] = json.loads(essay.comments)
                else:
                    essayDict['comments'] = ""
                essaysArray.append(essayDict)
            path = os.path.join(os.path.dirname(__file__), '../views' , 'essays.html')
            self.response.out.write(
                    template.render(path,locals())
                )
            
    def getMyRatings(self,ratingsJSON,curentUser):
        if ratingsJSON:
            objRatings = json.loads(ratingsJSON)
            ratingsArray = objRatings['data']
            for objRating in ratingsArray:
                if objRating['rated_by'] == curentUser.id:
                    return objRating['rating_points']
            return 0
        else:
            return 0
            
############################################################################################
#                    Save Rating Request handler
############################################################################################

class SaveRatings(webapp.RequestHandler):
    def post(self):
        ratingPoints = self.request.get('rate')
        essayID = self.request.get('idBox')
        currentUser = user.getUserbyId(user.getLoggedInUser())
        responseDict = {}
        if(not currentUser):
            responseDict['code'] = USER_NOT_LOGGEDIN_CODE
            responseDict['message'] = USER_NOT_LOGGED_IN_MSG
            self.response.out.write(json.dumps(responseDict))
        else:
            objEssay = Essay.get(essayID)
            ratingsJSON = objEssay.ratings
            if not self.hasRated(ratingsJSON,currentUser):
                currentRating = {}
                currentRating['rated_by'] = currentUser.id
                currentRating['rating_points'] = float(ratingPoints)
                time = datetime.now()
                currentRating['created'] = time.strftime("%b %d %Y %H:%M:%S")               
                if not ratingsJSON:
                    finalJSON = {}
                    ratingsArray = []
                    ratingsArray.append(currentRating)
                    finalJSON['data'] = ratingsArray
                    finalJSON['count'] = len(ratingsArray)
                    finalJSON['aggregate_rating'] = currentRating['rating_points']
                    objEssay.ratings = json.dumps(finalJSON)
                    objEssay.put()
                else:
                    finalJSON = json.loads(objEssay.ratings)
                    ratingsArray = finalJSON['data']
                    ratingsArray.append(currentRating)
                    finalJSON['data'] = ratingsArray
                    finalJSON['count'] = len(ratingsArray)
                    finalJSON['aggregate_rating'] = self.getAggregateRating(ratingsArray)
                    objEssay.ratings = json.dumps(finalJSON)
                    objEssay.put()           
                responseDict['code'] = SUCCESS_CODE
                responseDict['message'] = RATING_SUCCESS_MSG
                self.response.out.write(json.dumps(responseDict))
            else:
                responseDict['code'] = ALREADY_RATED_CODE
                responseDict['message'] = ALREADY_RATED_MSG
                self.response.out.write(json.dumps(responseDict))
                
            
    def hasRated(self,ratingsJSON,curentUser):
        if ratingsJSON:
            objRatings = json.loads(ratingsJSON)
            flag = False
            ratingsArray = objRatings['data']
            for objRating in ratingsArray:
                if objRating['rated_by'] == curentUser.id:
                    flag = True
            return flag
        else:
            return False
    
    def getAggregateRating(self,ratingsArray):
        totalPoints = 0
        for rating in ratingsArray:
            totalPoints += float(rating['rating_points'])

        return totalPoints/len(ratingsArray)    
            
################################################################################################
#                      Add Comment Request Handler
################################################################################################        
                
class AddComment(webapp.RequestHandler):
    def post(self):
        currentUser = user.getUserbyId(user.getLoggedInUser())
        responseDict = {}
        if(not currentUser):
            responseDict['code'] = USER_NOT_LOGGEDIN_CODE
            responseDict['message'] = USER_NOT_LOGGED_IN_MSG
            self.response.out.write(json.dumps(responseDict))
        else:
            commentText = self.request.get('comment')
            essayID = self.request.get('essay_id')
            userID = currentUser.id
            objEssay = Essay.get(essayID)
            commentsJSON = objEssay.comments
            commentDict = {}
            commentDict['comment_text'] = commentText
            commentDict['comment_by'] = userID
            commentDict['created'] = datetime.now().strftime("%b %d %Y %H:%M:%S")
            if not commentsJSON:
                finalJSON = {}
                commentsArray = []
                commentsArray.append(commentDict)
                finalJSON['count'] = len(commentsArray)
                finalJSON['data'] = commentsArray
                objEssay.comments = json.dumps(finalJSON)
                objEssay.put()
            else:
                finalJSON = json.loads(commentsJSON)
                commentsArray = finalJSON['data']
                commentsArray.append(commentDict)
                finalJSON['count'] = len(commentsArray)
                objEssay.comments = json.dumps(finalJSON)
                objEssay.put()
            responseDict['code'] = SUCCESS_CODE
            responseDict['message'] = COMMENT_ADDED_MSG
            self.response.out.write(json.dumps(responseDict))
                
###################################################################################################
#                         End ADD COMMENT HANDLER
###################################################################################################