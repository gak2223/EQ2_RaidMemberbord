# -*- coding: utf-8 -*-

from google.appengine.ext import webapp, db
import datetime
from jst import JST

def isMobile(webapp):
	#for s in ['Android', 'iPhone', 'iPod', 'iPad']:
	for s in ['Android', 'iPhone', 'iPod', 'iPad', 'Chrome', 'Firefox']:
		if(str(webapp.request.headers).find(s) > -1): return True
	return False
	#return True

def split_text(s, multiple):
	import textwrap
	return textwrap.fill(s, width=int(multiple))

def getNextDonichiDate(d):
	for n in range(0, 7):
		sonohi = d + datetime.timedelta(n)
		if(sonohi.weekday() in (5,6)):
			return sonohi.strftime('%Y-%m-%d') 
	return ''

def getBeforeDonichiDate(d):
	for n in range(0, 7):
		sonohi = d + datetime.timedelta(n * -1)
		if(sonohi.weekday() in (5,6)):
			return sonohi.strftime('%Y-%m-%d') 
	return ''

def sukatsuo():
	d = dict((x, u'スカウト') for x in range(60))
	d[5] = u'スカツオ'
	d[15] = u'スカツオ'
	d[25] = u'スカツオ'
	d[35] = u'スマスオ'
	d[45] = u'スカツオ'
	d[55] = u'スカツオ'
	return d.get(int(datetime.datetime.now(JST()).strftime('%S')))

class Comment(db.Model):
	kaisaibi = db.StringProperty()
	chara_name = db.StringProperty()
	chara_class = db.StringProperty()
	sanka = db.StringProperty()
	comment_text = db.StringProperty(multiline=True)
	tourokudate_text = db.StringProperty()
	tourokudate = db.DateTimeProperty()
	class_id = db.IntegerProperty()
	kakutoku_text = db.StringProperty(multiline=True)
	bgcolor = db.StringProperty()

class ClassList:
	flist = ['GRD', 'BSK', 'PAL', 'SK',  'MNK', 'BRU']
	fname = [u'ガーディアン', u'バーサーカー', u'パラディン', u'シャドウナイト',  u'モンク', u'ブルーザー']
	slist = ['RNG', 'ASN', 'SWB', 'BRG', 'TRB', 'DRG', 'BST']
	sname = [u'レンジャー', u'アサシン', u'スワッシュバッグラー', u'ブリガンド', u'トルバドール', u'ダージ', u'ビーストロード']
	plist = ['TMP', 'INQ', 'WDN', 'FRY', 'MST', 'DFL']
	pname = [u'テンブラー', u'インクイジター', u'ウォーデン', u'フューリー', u'ミスティック', u'デファイラー']
	mlist = ['WIZ', 'WLK', 'CNJ', 'NEC', 'ILL', 'CRC']
	mname = [u'ウィザード', u'ウォーロック', u'コンジュラー', u'ネクロマンサー', u'イリュージョニスト', u'コーアーサー']
	alist = flist + slist + plist + mlist
	aname = fname + sname + pname + mname
	clscolor = {'GRD': '#FFC0CB', 'BSK': '#FFC0CB', 'PAL': '#FFE4E1', 'SK': '#FFE4E1',  'MNK': '#FFF0F5', 'BRU': '#FFF0F5', 
				'RNG': '#FFE4B5', 'ASN': '#FFE4B5', 'SWB': '#FAEBD7', 'BRG': '#FAEBD7', 'TRB': '#FAF0E6', 'DRG': '#FAF0E6', 'BST': '#FFF8DC', 
				'TMP': '#8FBC8F', 'INQ': '#8FBC8F', 'WDN': '#98FB98', 'FRY': '#98FB98', 'MST': '#ADFF2F', 'DFL': '#ADFF2F', 
				'WIZ': '#ADD8E6', 'WLK': '#ADD8E6', 'CNJ': '#AFEEEE', 'NEC': '#AFEEEE', 'ILL': '#F0F8FF', 'CRC': '#F0F8FF'}

class Kaisaibi:
	def __init__(self, disp, kaisaibi, color):
		self.disp = disp
		self.kaisaibi = kaisaibi
		self.color = color

class TagTool:
	def __init__(self, clsname, snk):
		self.clsname = clsname
		self.snk = snk
	
	def GetClassname(self, clsid):
		return ClassList.aname[ClassList.alist.index(clsid)]

	def getClsTag(self):
		clstag = ''
		clstag += self.getClsTagDetail(ClassList.flist, u'Fighter')
		clstag += self.getClsTagDetail(ClassList.slist, u'Scout')
		clstag += self.getClsTagDetail(ClassList.plist, u'Prist')
		clstag += self.getClsTagDetail(ClassList.mlist, u'Mage')
		return clstag
		
	def getClsTagDetail(self, clslist, lbl):
		clstag = ''
		clstag += '<optgroup label="' + lbl + '">\n'
		for cls in (clslist):
			clstag += '\t'
			if(cls == self.clsname):
				#clstag += '<option value="' + cls + '" SELECTED />' + self.GetClassname(cls) + '\n'
				clstag += '<option value="' + cls + '" SELECTED >' + cls + '</option>\n'
			else:
				#clstag += '<option value="' + cls + '"/>' +  self.GetClassname(cls) + '\n'
				clstag += '<option value="' + cls + '">' +  cls + '</option>\n'
		clstag += '</optgroup>\n'
		return clstag

#	def getSankaTag(self):
#		snktag = ''
#		snklist = [u'参加', u'遅刻', u'お休み']
#		for sanka in (snklist):
#			if(sanka == self.snk):
#				snktag += '<option value="' + sanka + '" SELECTED />' + sanka + '\n'
#			else:
#				snktag += '<option value="' + sanka + '" />' + sanka + '\n'
#		return snktag

	def getSankaTag(self):
		n = 0
		snktag = ''
		snk = self.snk
		snklist = [u'参加', u'遅刻', u'お休み']
		if(len(snk) < 1): snk = snklist[0]
		for sanka in (snklist):
			n += 1
			if(sanka == snk):
				snktag += '<input type="radio" name="sanka" id="radio-' + str(n) + '" value="' + sanka + '" CHECKED /> ' + '\n'
			else:
				snktag += '<input type="radio" name="sanka" id="radio-' + str(n) + '" value="' + sanka + '" /> ' + '\n'
			snktag += '<label for="radio-' + str(n) + '">' + sanka + '</label> ' + '\n'
		return snktag

	def getDonichiTag(self):
		kyou = datetime.datetime.now(JST())
		b = False
		lst = []
		for n in range(-30, 8):
			if(n == 0):
				b = True
			sonohi = kyou + datetime.timedelta(n)
			if(sonohi.weekday() == 5):
				if(b):
					lst.append('<option value="' + sonohi.strftime('%Y-%m-%d') + '" STYLE="background-color:#B0C4DE" SELECTED/>' + sonohi.strftime('%Y-%m-%d') + u'(土)' + '\n')
					b = False
				else: 
					lst.append('<option value="' + sonohi.strftime('%Y-%m-%d') + '" STYLE="background-color:#B0C4DE"/>' + sonohi.strftime('%Y-%m-%d') + u'(土)' + '\n')
			elif (sonohi.weekday() == 6):
				if(b):
					lst.append('<option value="' + sonohi.strftime('%Y-%m-%d') + '" STYLE="background-color:#FFB6C1" SELECTED/>' + sonohi.strftime('%Y-%m-%d') + u'(日)' + '\n')
					b = False
				else:
					lst.append('<option value="' + sonohi.strftime('%Y-%m-%d') + '" STYLE="background-color:#FFB6C1"/>' + sonohi.strftime('%Y-%m-%d') + u'(日)' + '\n')
		donichitag = ''
		for s in reversed(lst):
			donichitag += s
		return donichitag

