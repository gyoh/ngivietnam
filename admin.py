#!/usr/bin/env python
# encoding: utf-8
"""
admin.py

Created by Gyo Hamamoto on 2008-09-12.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import wsgiref.handlers

from google.appengine.api import datastore
from google.appengine.api import datastore_types
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from model import *

class Image(webapp.RequestHandler):
    def get(self):
        news = db.get(self.request.get("news_id"))
        if news.image:
            self.response.headers['Content-Type'] = "image/jpg"
            self.response.out.write(news.image)
        else:
            self.error(404)

class NewsPage(webapp.RequestHandler):
    def get(self):
        newslist = News.all()
        newslist.order("-posted")
        path = os.path.join(os.path.dirname(__file__), 'templates/admin/news.html')
        self.response.out.write(template.render(path, {'newslist': newslist}, debug = True))
 
    def post(self):
        news = News()
        news.title = self.request.get('title')
        news.content = db.Text(self.request.get('content'))
        posted = self.request.get('posted')
        #news.posted = self.request.get('posted')
        news.link = db.Link(self.request.get('link'))
        #news.tags = self.request.get('tags')
        #news.image = db.Blob(self.request.get('image'))
        news.language = self.request.get('language')
        news.public = bool(int(self.request.get('public')))
        news.put()
        self.redirect('/admin/news')

class JobsPage(webapp.RequestHandler):
    def get(self):
        jobs = Job.all()
        jobs.order("-posted")
        path = os.path.join(os.path.dirname(__file__), 'templates/admin/jobs.html')
        self.response.out.write(template.render(path, {'jobs': jobs}, debug = True))

    def post(self):
        job = Job()
        job.title = self.request.get('title')
        job.unit = self.request.get('unit')
        job.location = self.request.get('location')
        #job.posted = self.request.get('posted')
        job.responsibilities = self.request.get('responsibilities')
        job.qualifications = self.request.get('qualifications')
        job.desired = self.request.get('desired')
        job.salary = self.request.get('salary')
        job.general = self.request.get('general')
        job.language = self.request.get('language')
        job.public = bool(int(self.request.get('public')))
        job.put()
        self.redirect('/admin/jobs')

def main():
    application = webapp.WSGIApplication([('/admin/news', NewsPage),
        ('/admin/jobs', JobsPage)], debug = True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()

