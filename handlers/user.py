from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from models.Models import User
import os
import email
import json

providers = {
    'Google'   : 'https://www.google.com/accounts/o8/id',
    'Yahoo'    : 'yahoo.com',
    'MySpace'  : 'myspace.com',
    'AOL'      : 'aol.com',
    'MyOpenID' : 'myopenid.com'
    # add more here
}

class LoginPageHandler(webapp.RequestHandler):
    def get(self):
            self.response.out.write('Hello world! Sign in at: ')
            for name, uri in providers.items():
                self.response.out.write('[<a href="%s">%s</a>]' % (
                    users.create_login_url(dest_url='/complete_profile',federated_identity=uri), name))
                
class FirstTimeUserHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            myUser = User.all().filter('email = ', user.email())
            if(myUser.count() >=1):
                userMetaData = json.loads(myUser[0].metadata)
                self.response.out.write(userMetaData)
                if userMetaData['profile_completed'] == 0 :
                    self.redirect('/completeProfile')
            else:
                userDict ={}
                userDict['is_first_time'] = 1;
                userDict['profile_completed'] = 0;
                email = user.email()
                new_user = User()
                new_user.email = email;
                new_user.metadata = json.dumps(userDict)
                new_user.put()
                path = os.path.join(os.path.dirname(__file__), '../views' , 'complete_profile.html')
                self.response.out.write(
                  template.render(path,locals())
            )
        else:
            self.redirect('/')
            
class DoCompleteProfile(webapp.RequestHandler):
    def post(self):
        nickname = self.request.get('nickname')
        aboutme = self.request.get('about-me')
        userEmail = self.request.get('email')
        users = User.all().filter('email = ', userEmail)
        for user in users:
            if(user):
                userMetaData = json.loads(user.metadata)
                if(userMetaData['is_first_time']):
                    userMetaData['profile_completed'] = 1;
                    userMetaData['is_first_time'] = 0;
                    user.nickname = nickname
                    user.aboutme = aboutme
                    user.metadata = json.dumps(userMetaData)
                    user.put()
                    self.redirect('/home')
                else:
                    self.redirect('/profile')
            else:
                self.response.out.write("no user with this email found, Please try to login again")
                