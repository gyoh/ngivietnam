from google.appengine.ext import db

class News(db.Model):
    title = db.StringProperty(multiline = False, default = '')
    content = db.TextProperty(default = '')
    posted = db.DateProperty(auto_now_add = True)
    link = db.LinkProperty()
    tags = db.ListProperty(db.Category)
    image = db.BlobProperty()
    language = db.StringProperty(required = True, choices = set(['en', 'ja', 'vi']), default = 'en')
    public = db.BooleanProperty(default = False)

class Job(db.Model):
    title = db.StringProperty(multiline = False, default = '')
    unit = db.StringProperty(multiline = False, default = '')
    location = db.StringProperty(multiline = False, default = '')
    posted = db.DateProperty(auto_now_add = True)
    responsibilities = db.TextProperty(default = '')
    qualifications = db.TextProperty(default = '')
    desired = db.TextProperty(default = '')
    salary = db.StringProperty(default = '')
    general = db.TextProperty(default = '')
    language = db.StringProperty(required = True, choices = set(['en', 'ja', 'vi']), default = 'en')
    public = db.BooleanProperty(default = False)

class Entry():
    title = None
    updated = None
    link = None