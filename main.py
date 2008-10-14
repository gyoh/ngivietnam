#!/usr/bin/env python
#
# Copyright 2008 ngi vietnam Co., Ltd.
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

"ngi vietnam corporate website"

__author__ = 'Gyo Hamamoto'

import cgi
import datetime
import logging
import os
import re
import sys
import urllib
import urlparse
import wsgiref.handlers

from google.appengine.api import datastore
from google.appengine.api import datastore_types
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from model import *

import gdata.alt.appengine
import gdata.blogger.service

# Set to true if we want to have our webapp print stack traces, etc
_DEBUG = True

class BaseController(webapp.RequestHandler):
    """Supplies a common template generation function."""

    def setlang(self):
        # Set language by path
        if re.compile("\/ja/.*").match(self.request.path):
            self.lang = 'ja'
            self.path = self.request.path[3:]
        elif re.compile("\/vi/.*").match(self.request.path):
            self.lang = 'vi'
            self.path = self.request.path[3:]
        else:
            self.lang = 'en'
            self.path = self.request.path

    """
    When you call render(), we augment the template variables supplied with
    the current user in the 'user' variable and the current webapp request
    in the 'request' variable.
    """
    def render(self, template_name, template_values = {}):
        # Set values to pass on to templates
        values = {
            'request': self.request,
            'user': users.GetCurrentUser(),
            'login_url': users.CreateLoginURL(self.request.uri),
            'logout_url': users.CreateLogoutURL(self.request.uri),
            'application_name': 'ngi vietnam corporate website',
            'lang': self.lang,
            'path': self.path
        }
        values.update(template_values)

        # Render template based on the defined language
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, os.path.join('templates', template_name))
        if self.lang == 'ja' or self.lang == 'vi':
            path = path + '.' + self.lang
        self.response.out.write(template.render(path, values, debug = _DEBUG))
    
    def error(self, errorcode, message = 'an error occured'):
        self.setlang()
        if errorcode == 404:
            self.render('404.html', {})
        if errorcode == 500:
            self.render('500.html', {})

class MainPage(BaseController):
    def get(self):
        self.setlang()
        newslist = News.all()
        newslist.filter('language', self.lang)
        newslist.filter('public', True)
        newslist.order('-posted')
        newslist.fetch(10)
        self.render('index.html', {'newslist': newslist, 'newscount': newslist.count()})

class Service(BaseController):
    def get(self):
        self.setlang()
        self.render('services.html', {})

class ServiceContact(BaseController):
    def get(self):
        self.setlang()
        self.render('services_contact.html', {})

    def post(self):
        self.setlang()
        self.render('services_contact.html', {})

class ServiceContactConfirmEmail(BaseController):
    def get(self):
        self.setlang()
        self.redirect('/service/contact')

    def post(self):
        self.setlang()
        sender = self.request.get('email')
        if mail.is_email_valid(sender):
            self.render('services_confirm_email.html', {})
        else:
            self.render('services_contact.html', {'error': 'Invalid address.'})

class ServiceContactSendEmail(BaseController):
    def get(self):
        self.setlang()
        self.redirect('/service/contact')
        
    def post(self):
        self.setlang()
        submit = self.request.get('Submit')
        if submit == 'Edit':
            self.render('services_contact.html', {})
        elif submit == 'Send':
            sender = 'gyo@ngivietnam.com'
            to = 'contact@ngivietnam.com'
            subject = "[Services] " + self.request.get('subject')
            body = "Sender: "+ self.request.get('email') + "\nMessage:\n" + self.request.get('body')
            try:
                mail.send_mail(sender, to, subject, body)
                self.render('services_send_email.html', {})
            except:
                self.error(500)
        else:
            self.error(404)

class Press(BaseController):
    def get(self):
        self.setlang()
        newslist = News.all()
        newslist.filter('language', self.lang)
        newslist.filter('public', True)
        newslist.order('-posted')
        
        self.service = gdata.blogger.service.BloggerService()
        gdata.alt.appengine.run_on_appengine(self.service)
        feed = None
        try:
            query = gdata.blogger.service.BlogPostQuery()
            query.feed = 'http://blog.ngivietnam.com/feeds/posts/default'
            query.orderby = 'updated'
            query.max_results = 10
            feed = self.service.Get(query.ToUri())            
            #feed = self.service.GetBlogPostFeed(None, 'http://blog.ngivietnam.com/feeds/posts/default')
        except Exception:
            logging.error('Failed to get blog post feed.')

        entries = []
        if feed is not None:
            for feed_entry in feed.entry:
                entry = Entry()
                entry.title = feed_entry.title.text
                entry.updated = feed_entry.updated.text[0:10]
                entry.link = feed_entry.GetHtmlLink().href
                entries.append(entry)

        self.render('press.html', {'newslist': newslist, 'newscount': newslist.count(), 'entries': entries, 'entrycount': len(entries)})

class Company(BaseController):
    def get(self):
        self.setlang()
        self.render('profile.html', {})

class CompanyMission(BaseController):
    def get(self):
        self.setlang()
        self.render('mission.html', {})

class CompanyBusiness(BaseController):
    def get(self):
        self.setlang()
        self.render('business.html', {})

class Recruit(BaseController):
    def get(self):
        self.setlang()
        jobs = Job.all()
        jobs.filter('language', self.lang)
        jobs.filter('public', True)
        jobs.order('-posted')
        self.render('jobs.html', {'jobs': jobs, 'jobcount': jobs.count()})

class RecruitContact(BaseController):
    def get(self):
        self.setlang()
        self.render('jobs_contact.html', {})
    
    def post(self):
        self.setlang()
        self.render('jobs_contact.html', {})

class RecruitContactConfirmEmail(BaseController):
    def get(self):
        self.setlang()
        self.redirect('/recruit/contact')

    def post(self):
        self.setlang()
        sender = self.request.get('email')
        if mail.is_email_valid(sender):
            self.render('jobs_confirm_email.html', {})
        else:
            self.render('jobs_contact.html', {'error': 'Invalid address.'})

class RecruitContactSendEmail(BaseController):
    def get(self):
        self.setlang()
        self.redirect('/recruit/contact')

    def post(self):
        self.setlang()
        submit = self.request.get('Submit')
        if submit == 'Edit':
            self.render('jobs_contact.html', {})
        elif submit == 'Send':
            sender = 'gyo@ngivietnam.com'
            to = 'contact@ngivietnam.com'
            subject = "[Jobs] " + self.request.get('subject')
            body = "Sender: "+ self.request.get('email') + "\nMessage:\n" + self.request.get('body')
            try:
                mail.send_mail(sender, to, subject, body)
                self.render('jobs_send_email.html', {})
            except:
                self.error(500)
        else:
            self.error(404)

class Sitemap(BaseController):
    def get(self):
        self.setlang()
        self.render('sitemap.html', {})

class ErrorPage(BaseController):
    def get(self):
        self.error(404)

    def post(self):
        self.error(404)

def main():
    application = webapp.WSGIApplication([('/', MainPage),
        ('/ja/', MainPage),
        ('/vi/', MainPage),
        ('/service', Service),
        ('/ja/service', Service),
        ('/vi/service', Service),
        ('/service/contact', ServiceContact),
        ('/ja/service/contact', ServiceContact),
        ('/vi/service/contact', ServiceContact),
        ('/service/contact/confirmemail', ServiceContactConfirmEmail),
        ('/ja/service/contact/confirmemail', ServiceContactConfirmEmail),
        ('/vi/service/contact/confirmemail', ServiceContactConfirmEmail),
        ('/service/contact/sendemail', ServiceContactSendEmail),
        ('/ja/service/contact/sendemail', ServiceContactSendEmail),
        ('/vi/service/contact/sendemail', ServiceContactSendEmail),
        ('/press', Press),
        ('/ja/press', Press),
        ('/vi/press', Press),
        ('/company', Company),
        ('/ja/company', Company),
        ('/vi/company', Company),
        ('/company/mission', CompanyMission),
        ('/ja/company/mission', CompanyMission),
        ('/vi/company/mission', CompanyMission),
        ('/company/business', CompanyBusiness),
        ('/ja/company/business', CompanyBusiness),
        ('/vi/company/business', CompanyBusiness),
        ('/recruit', Recruit),
        ('/ja/recruit', Recruit),
        ('/vi/recruit', Recruit),
        ('/recruit/contact', RecruitContact),
        ('/ja/recruit/contact', RecruitContact),
        ('/vi/recruit/contact', RecruitContact),
        ('/recruit/contact/confirmemail', RecruitContactConfirmEmail),
        ('/ja/recruit/contact/confirmemail', RecruitContactConfirmEmail),
        ('/vi/recruit/contact/confirmemail', RecruitContactConfirmEmail),
        ('/recruit/contact/sendemail', RecruitContactSendEmail),
        ('/ja/recruit/contact/sendemail', RecruitContactSendEmail),
        ('/vi/recruit/contact/sendemail', RecruitContactSendEmail),
        ('/sitemap', Sitemap),
        ('/ja/sitemap', Sitemap),
        ('/vi/sitemap', Sitemap),
        ('/.*', ErrorPage)],
        debug = _DEBUG)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
