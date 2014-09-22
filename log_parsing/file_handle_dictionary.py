#!/usr/bin/python

import os
import sys
import logging
import traceback
from collections import OrderedDict
from collections import MutableMapping

class FileHandleDict(MutableMapping):
	def __init__(self, limit):
	        self.store = OrderedDict()
		self.limit = limit

    	def __getitem__(self, key):
        	val = self.store[key]
		# Push value to the top of the order
		del self.store[key]
		self.store[key] = val
		return val

    	def __setitem__(self, key, val):
		# Replace existing file handle
		if key in self.store:
			# File handle hasn't changed.
			if self.store[key] == val:
				return
			self.store[key].close()
			del self.store[key]

		# Adding a new key would put us over limit
		if len(self.store) >= self.limit:
			k, fh = self.store.popitem(last=False)
			fh.close()

        	self.store[key] = val

	def __delitem__(self, key):
       		del self.store[key]

    	def __iter__(self):
        	return iter(self.store)

    	def __len__(self):
        	return len(self.store)

	def __contains__(self, key):
		return key in self.store

	def close_all(self):
		for val in self.store.itervalues():
			val.close()
		self.store.clear()

# Testing code
if __name__ == "__main__":
	fhd = FileHandleDict(3)
	fhd[1] = open('/home/kyle/table.in', 'r')
	print fhd.keys()
	fhd[2] = open('/home/kyle/table1.in', 'r')
	print fhd.keys()
	fhd[3] = open('/home/kyle/table2.in', 'r')
	print fhd.keys()
	fhd[4] = open('/home/kyle/table3.in', 'r')
	print fhd.keys()
	a = fhd[3]
	print fhd.keys()
	print 2 in fhd
	print fhd.keys()
	fhd.close_all()
