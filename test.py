# -*- coding: utf-8 -*-

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
import os
import datetime
import define
from jst import JST
from define import Comment
from define import TagTool
from jst import JST

class MainHandler(webapp.RequestHandler):
    def get(self):
		s = u""
		s += str(self.request.headers)
		s += u'<br>'
		s += u'<br>'
		if(define.isMobile(self)):
			s += u"smartphone"
		else:
			s += u"pc"
		self.response.out.write(s)

def main():
	application = webapp.WSGIApplication([
		('/.*', MainHandler),
	],
	debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()
