# -*- coding: utf-8 -*-

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
import os
import datetime
from jst import JST
import define
from define import Comment
from define import TagTool
from jst import JST

class PostHandler(webapp.RequestHandler):
	def post(self):
		b = 1
		kyou = datetime.datetime.now(JST()).strftime('%Y-%m-%d')
		year = int(kyou[0:4])
		month = int(kyou[5:7])
		if((month - b) < 1):
			month = month + 12 - b
			year -= 1
		else:
			month -= b
		sonohi = datetime.date(year, month, 1).strftime('%Y-%m-%d')
		for s in Comment.gql(' WHERE kaisaibi < :kaisaibi', kaisaibi = sonohi):
			s.delete()
		try:
			ymd = self.request.get('kaisaibi').split('-')
			theday = datetime.date(int(ymd[0]), int(ymd[1]), int(ymd[2]))
		except ValueError:
			theday = datetime.datetime.now(JST())
		self.redirect('/insert?kaisaibi=' + theday.strftime('%Y-%m-%d'))

class MainHandler(webapp.RequestHandler):
	def get(self):
		import define
		TZ = JST()
		kyou = datetime.datetime.now(TZ)
		tt = TagTool('', '')
		template_values = {'donichitag': tt.getDonichiTag(), 
							'defdate': define.getNextDonichiDate(datetime.datetime.now(JST())),
						  }
		#path = os.path.join(os.path.dirname(__file__), 'templates/main.html')
		path = os.path.join(os.path.dirname(__file__), 'templates/mains.html' if define.isMobile(self) else 'templates/main.html')
		self.response.out.write(template.render(path, template_values))

class ElseHandler(webapp.RequestHandler):
	def get(self):
		self.redirect('/insert?kaisaibi=' + define.getNextDonichiDate(datetime.datetime.now(JST())))

def main():
	application = webapp.WSGIApplication([
		('/post', PostHandler),
		('/', MainHandler),
		('/.*', ElseHandler),
	],
	debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()
