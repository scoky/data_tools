#!/usr/bin/python

import os
import sys
import logging
import traceback
import re
from urlparse import urlparse
from parse_logs import LineParser

class O2Parser(LineParser):
	def __init__(self):
		self.compress = re.compile('(\d+)\s*->\s*(\d+)\s+(-?\d+)%\s*(\w+)')
		pass

	def parse(self, line):
		chunks = line.rstrip().split()
		url = chunks[-1].strip('|')
		domain = urlparse(url).netloc
		if not domain.endswith('googlevideo.com') and not domain.endswith('facebook.com'):
			return EmptyLine()
		
		pre_size = post_size = ratio = hit = '?'
		match = self.compress.search(line)
		if match:
			pre_size = match.group(1)
			post_size = match.group(2)
			ratio = match.group(3)
			hit = 'HIT' in match.group(4)
		
		return O2Line(domain, pre_size, post_size, ratio, hit)

class O2Line(object):
	def __init__(self, url, pre_size, post_size, ratio, hit):
		self.url = url
		self.pre_size = pre_size
		self.post_size = post_size
		self.ratio = ratio
		self.hit = hit

	def output(self):
		return self.url+' '+self.pre_size+' '+self.post_size+' '+self.ratio+' '+str(self.hit)+'\n'

class EmptyLine(object):
	def output(self):
		return ''
