# -*- coding: utf-8 -*-

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

import os
import datetime
import time
from jst import JST
import logging
import define
from define import Comment
from define import TagTool
from define import ClassList


class PostHandler(webapp.RequestHandler):
	def post(self):
		try:
			c = Comment()
			c.kaisaibi = self.request.get('kaisaibi')
			c.chara_name = self.request.get('chara_name')
			c.chara_class = self.request.get('chara_class')
			c.sanka = self.request.get('sanka')
			c.comment_text = self.request.get('comment_text')
			c.tourokudate_text = datetime.datetime.now(JST()).strftime('%Y-%m-%d %H:%M:%S')
			c.tourokudate = datetime.datetime.now(JST())
			c.class_id = ClassList.alist.index(c.chara_class)
			c.put()
			if(self.request.get('onaji') == 'yes'):
				c = Comment()
				c.kaisaibi = (datetime.datetime.strptime(self.request.get('kaisaibi'), '%Y-%m-%d') + datetime.timedelta(1)).strftime('%Y-%m-%d')
				c.chara_name = self.request.get('chara_name')
				c.chara_class = self.request.get('chara_class')
				c.sanka = self.request.get('sanka')
				c.comment_text = self.request.get('comment_text')
				c.tourokudate_text = datetime.datetime.now(JST()).strftime('%Y-%m-%d %H:%M:%S')
				c.tourokudate = datetime.datetime.now(JST())
				c.class_id = ClassList.alist.index(c.chara_class)
				c.put()
			# MainHandlerへリダイレクト
			self.redirect('/insert?kaisaibi=' + self.request.get('kaisaibi'))
		except:
			self.redirect('/')

class AddsHandler(webapp.RequestHandler):
	def get(self):
		try:
			ss = self.request.get('kaisaibi').split('-')
			youbi =  u"月 火 水 木 金 土 日".split()[datetime.datetime(int(ss[0]),int(ss[1]),int(ss[2])).weekday()]
			tt = TagTool('', '')
			template_values = {'kaisaibi': self.request.get('kaisaibi'), 
							   'youbi': youbi, 
							   'youbinum': datetime.datetime(int(ss[0]),int(ss[1]),int(ss[2])).weekday(),
							   'clstag': tt.getClsTag(),
							   'snktag': tt.getSankaTag(),
							  }
			path = os.path.join(os.path.dirname(__file__), 'templates/adds.html')
			self.response.out.write(template.render(path, template_values))
		except:
			self.redirect('/')

class MainHandler(webapp.RequestHandler):
	def get(self):
		try:
			sankaf, sankas, sankap, sankam, hoketsuf, hoketsus, hoketsup, hoketsum, yasumi = getSankaLists(self.request.get('kaisaibi'))
			ss = self.request.get('kaisaibi').split('-')
			#youbi =  u"日 月 火 水 木 金 土".split()[ datetime. datetime(int(ss[0]),int(ss[1]),int(ss[2])).isoweekday()]
			youbi =  u"月 火 水 木 金 土 日".split()[datetime.datetime(int(ss[0]),int(ss[1]),int(ss[2])).weekday()]
			tt = TagTool('', '')
			template_values = {'sankacnt': len(sankaf) + len(sankas)+ len(sankap)+len(sankam), 
							   'sankaf': sankaf, 
							   'sankafcnt': len(sankaf), 
							   'sankas': sankas, 
							   'sankascnt': len(sankas), 
							   'sankap': sankap, 
							   'sankapcnt': len(sankap), 
							   'sankam': sankam,
							   'sankamcnt': len(sankam),
							   'hoketsucnt':len(hoketsuf) + len(hoketsus) + len(hoketsup) + len(hoketsum), 
							   'hoketsuf': hoketsuf, 
							   'hoketsufcnt': len(hoketsuf), 
							   'hoketsus': hoketsus, 
							   'hoketsuscnt': len(hoketsus), 
							   'hoketsup': hoketsup, 
							   'hoketsupcnt': len(hoketsup), 
							   'hoketsum': hoketsum,
							   'hoketsumcnt': len(hoketsum),
							   'yasumi': yasumi,
							   'yasumicnt': len(yasumi),
							   'kaisaibi':self.request.get('kaisaibi'),
							   'youbi': youbi,
							   'clstag': tt.getClsTag(),
							   'snktag': tt.getSankaTag(),
							   'beforedate': define.getBeforeDonichiDate(datetime.datetime.strptime(self.request.get('kaisaibi'), '%Y-%m-%d') + datetime.timedelta(-1)),
							   'nearestdate': define.getNextDonichiDate(datetime.datetime.now(JST())),
							   'nextdate': define.getNextDonichiDate(datetime.datetime.strptime(self.request.get('kaisaibi'), '%Y-%m-%d') + datetime.timedelta(1)),
							   'sukatsuo': define.sukatsuo()
							  }
			#path = os.path.join(os.path.dirname(__file__), 'templates/insert.html')
			path = os.path.join(os.path.dirname(__file__), 'templates/inserts.html' if define.isMobile(self) else 'templates/insert.html')
			self.response.out.write(template.render(path, template_values))
		except:
			self.redirect('/')

def getSankaLists(kaisaibi):
	lst = []
	for n in range(9): lst.append([])
	for s in Comment.gql(' WHERE kaisaibi = :kaisaibi ORDER BY class_id, tourokudate_text ', kaisaibi = kaisaibi):
		#s.comment_text = define.split_text(s.comment_text, 20)
		s.bgcolor = ClassList.clscolor.get(s.chara_class.upper(), '')
		sanka = s.sanka
		if     (sanka == u'参加'):
			if   (s.chara_class.upper() in ClassList.flist): lst[0].append(s)
			elif (s.chara_class.upper() in ClassList.slist): lst[1].append(s)
			elif (s.chara_class.upper() in ClassList.plist): lst[2].append(s)
			elif (s.chara_class.upper() in ClassList.mlist): lst[3].append(s)
		elif (sanka == u'遅刻') or (sanka == u'補欠'):
			if   (s.chara_class.upper() in ClassList.flist): lst[4].append(s)
			elif (s.chara_class.upper() in ClassList.slist): lst[5].append(s)
			elif (s.chara_class.upper() in ClassList.plist): lst[6].append(s)
			elif (s.chara_class.upper() in ClassList.mlist): lst[7].append(s)
		elif (sanka == u'お休み'): lst[8].append(s)
	return lst[0], lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7], lst[8]

def main():
	application = webapp.WSGIApplication([
		('/insert', MainHandler),
		('/insert.*/', MainHandler),
		('/insert/post', PostHandler),
		('/adds', AddsHandler),
		],debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
