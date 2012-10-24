from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from models.Models import User
import os
#import email
import json

class LoginPageHandler(webapp.RequestHandler):
    def get(self):
        urlDict = {}
        urlDict['google'] = users.create_login_url(dest_url='/complete_profile',federated_identity="https://www.google.com/accounts/o8/id")
        urlDict['yahoo'] = users.create_login_url(dest_url='/complete_profile',federated_identity="yahoo.com")
        urlDict['aol'] = users.create_login_url(dest_url='/complete_profile',federated_identity="aol.com")
        urlDict['myopenid'] = users.create_login_url(dest_url='/complete_profile',federated_identity="myopenid.com")
        path = os.path.join(os.path.dirname(__file__), '../views' , 'login.html')
        self.response.out.write(template.render(path,locals()))
                
class FirstTimeUserHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        user_id = user.user_id()
        email = user.email()
        if user:
            myUser = User.all().filter('id = ',user_id)
            if(myUser.count() >= 1):
                userMetaData = json.loads(myUser[0].metadata)
                if (userMetaData['profile_completed'] == 0):
                    path = os.path.join(os.path.dirname(__file__), '../views' , 'complete_profile.html')
                    self.response.out.write(template.render(path,locals()))
                else:
                    self.redirect('/home')
            else:
                userDict ={}
                userDict['is_first_time'] = 1;
                userDict['profile_completed'] = 0;
                new_user = User()
                new_user.id = user_id
                new_user.email = email;
                new_user.metadata = json.dumps(userDict)
                new_user.put()
                path = os.path.join(os.path.dirname(__file__), '../views' , 'complete_profile.html')
                self.response.out.write(
                  template.render(path,locals())
                  )
        else:
            self.redirect('/login')

class DoCompleteProfile(webapp.RequestHandler):
    def post(self):
        current_user = users.get_current_user()
        if(not current_user):
            self.redirect('/login')
        else:
            user_id = current_user.user_id()
            nickname = self.request.get('nickname')
            aboutme = self.request.get('about-me')
            allusers = User.all().filter('id = ',user_id)
            for user in allusers:
                if(user):
                    userMetaData = json.loads(user.metadata)
                    if(userMetaData['is_first_time']):
                        userMetaData['profile_completed'] = 1
                        userMetaData['is_first_time'] = 0
                        user.nickname = nickname
                        user.aboutme = aboutme
                        user.metadata = json.dumps(userMetaData)
                        user.put()
                        self.redirect('/home')
                    else:
                        self.redirect('/home')
                else:
                    self.response.out.write("Sorry something went wrong, Please try again")
                    
class HomeHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/login')
        else:
            currentUser = getUserbyId(user.user_id())
            if(currentUser):
                userName = currentUser.nickname
                path = os.path.join(os.path.dirname(__file__), '../views' , 'home.html')
                self.response.out.write(
                  template.render(path,locals())
                  )
            else:
                self.response.out.write("Your record cannot be found from DB Please try to login again")
                
                
                

def getUserbyId(user_id):
    if not user_id:
        return False;
    myUser = User.all().filter('id = ',user_id)
    if(myUser):
        return myUser[0]
    else:
        return False

def getLoggedInUser():
    user = users.get_current_user()
    if user:
        return user.user_id()
    else:
        False;