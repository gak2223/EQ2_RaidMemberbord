# -*- coding: utf-8 -*-

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
import os
import datetime
import time
import calendar
import logging
from jst import JST
from define import Comment

class PostHandler(webapp.RequestHandler):
	def post(self):
		try:
			c = Comment.get_by_id(int(self.request.get('sankaid')))
			db.delete(c)
			# MainHandlerへリダイレクト
			self.redirect('/insert?kaisaibi=' + self.request.get('kaisaibi'))
		except:
			self.redirect('/')

class MainHandler(webapp.RequestHandler):
	def get(self):
		import define
		try:
			c = Comment.get_by_id(int(self.request.get('sankaid')))
			if(c is None): 
				self.redirect('/')
				return
			ss = c.kaisaibi.split('-')
			youbi =  u"月 火 水 木 金 土 日".split()[datetime.datetime(int(ss[0]),int(ss[1]),int(ss[2])).weekday()]
			template_values = {'data': c,
								'youbi': youbi,
							}
			#path = os.path.join(os.path.dirname(__file__), 'templates/delete.html')
			path = os.path.join(os.path.dirname(__file__), 'templates/deletes.html' if define.isMobile(self) else 'templates/delete.html')
			self.response.out.write(template.render(path, template_values))
		except:
			self.redirect('/')

def main():
	application = webapp.WSGIApplication([
		('/delete', MainHandler),
		('/delete.*/', MainHandler),
		('/delete/post', PostHandler),
	],
	debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()
