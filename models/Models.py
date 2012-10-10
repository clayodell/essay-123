from google.appengine.ext import db

class Topic(db.Model):
    #length limits to be finalized here also the default properties
    title = db.StringProperty() 
    description = db.TextProperty()
    access_type = db.IntegerProperty()
    tags = db.StringProperty()
    owner = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty()
    modifier = db.StringProperty()
    is_deleted = db.BooleanProperty()
    
class User(db.Model):
    email = db.StringProperty()
    nickname = db.StringProperty()
    aboutme = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    metadata = db.StringProperty()
    