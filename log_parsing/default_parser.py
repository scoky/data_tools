#!/usr/bin/python

import os
import sys
import logging
import traceback
from parse_logs import LineParser

class DefaultParser(LineParser):
	def __init__(self):
		self.counter = 0

	def parse(self, line):
		self.counter += 1
		chunks = line.rstrip().split()
		return ParsedLine(chunks, self.counter)

class ParsedLine(object):
	def __init__(self, chunks, counter):
		self.chunks = chunks
		self.counter = counter
