from google.appengine.ext import db

class User(db.Model):
    id = db.StringProperty()
    email = db.StringProperty()
    nickname = db.StringProperty()
    aboutme = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    metadata = db.StringProperty()
    
class Topic(db.Model):
    #length limits to be finalized here also the default properties
    title = db.StringProperty() 
    description = db.TextProperty()
    access_type = db.IntegerProperty()
    tags = db.StringProperty()
    owner = db.ReferenceProperty(User,collection_name = "user")
    created = db.DateTimeProperty(auto_now_add=True)
    history = db.TextProperty()
    is_deleted = db.BooleanProperty(default=False)
    visitors = db.StringProperty()
    deleteMetaData = db.StringProperty()
    
class Essay(db.Model):
    essay_text = db.TextProperty()
    owner = db.ReferenceProperty(User,collection_name = "authors")
    created = db.DateTimeProperty(auto_now_add=True)
    history = db.TextProperty()
    parent_topic = db.ReferenceProperty(Topic,collection_name="topic")
    is_deleted = db.BooleanProperty(default=False)
    deleteMetaData = db.StringProperty()