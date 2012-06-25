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
from define import TagTool

class PostHandler(webapp.RequestHandler):
	def post(self):
		try:
			c = Comment.get_by_id(int(self.request.get('sankaid')))
			c.kaisaibi = self.request.get('kaisaibi')
			c.chara_name = self.request.get('chara_name')
			c.chara_class = self.request.get('chara_class')
			c.sanka = self.request.get('sanka')
			c.comment_text = self.request.get('comment_text')
			c.tourokudate_text = datetime.datetime.now(JST()).strftime('%Y-%m-%d %H:%M:%S')
			c.tourokudate = datetime.datetime.now(JST())
			c.put()
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
			tt = TagTool(c.chara_class, c.sanka)
			ss = c.kaisaibi.split('-')
			#youbi =  u"日 月 火 水 木 金 土".split()[ datetime. datetime(int(ss[0]),int(ss[1]),int(ss[2])).isoweekday()]
			youbi =  u"月 火 水 木 金 土 日".split()[datetime.datetime(int(ss[0]),int(ss[1]),int(ss[2])).weekday()]
			template_values = {'data': c,
								'youbi': youbi,
								'clstag': tt.getClsTag(),
								'snktag': tt.getSankaTag(),
							}
			path = os.path.join(os.path.dirname(__file__), 'templates/edit.html')
			path = os.path.join(os.path.dirname(__file__), 'templates/edits.html' if define.isMobile(self) else 'templates/edit.html')
			self.response.out.write(template.render(path, template_values))
		except:
			self.redirect('/')

def main():
	application = webapp.WSGIApplication([
		('/edit', MainHandler),
		('/edit.*/', MainHandler),
		('/edit/post', PostHandler),
	],
	debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()
