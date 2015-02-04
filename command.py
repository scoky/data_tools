import sys
import os

class Command(object):
	def __init__(self, init, on_row, on_finish):
		self.init = init
		self.on_row = on_row
		self.on_finish = on_finish

	def arguments(self, args):
		pass

class PerformReturn(object):
	def __init__(self, action):
		self.action = action

	def perform(self, g, a, b):
		self.action(g, a, b)
		return a
