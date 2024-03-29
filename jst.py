# -*- coding: utf-8 -*-

import datetime

class JST(datetime.tzinfo):
  def utcoffset(self, dt):return datetime.timedelta(hours=9)
  def dst(self, dt):return datetime.timedelta(0)
  def tzname(self, dt):return "JDT"

class UTC(datetime.tzinfo):
  def utcoffset(self, dt):return datetime.timedelta(0)
  def tzname(self, dt):return "UTC"
  def dst(self, dt):return datetime.timedelta(0)