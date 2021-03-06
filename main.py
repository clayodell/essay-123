#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from handlers import index,topic,user,essay

        
application = webapp.WSGIApplication([
    ('/',index.IndexHandler),
    ('/register',index.RegisterHandler),
    ('/create-topic',topic.CreateTopic),
    ('/do-add_topic',topic.DoAddTopic),
    ('/topics',topic.viewPublicTopics),
    ('/login',user.LoginPageHandler),
    ('/complete_profile',user.FirstTimeUserHandler),
    ('/do_complete_profile',user.DoCompleteProfile),
    ('/edit-topic',topic.editTopic),
    ('/do-edit-topic',topic.doEditTopic),
    ('/home',user.HomeHandler),
    ('/delete-topic',topic.DoDeleteTopic),
    ('/new-essay',essay.NewEssay),
    ('/create-essay',essay.CreateEssay),
    ('/essays',essay.ShowEssays),
    ('/save-essay-rating',essay.SaveRatings),
    ('/add-comment',essay.AddComment)
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
