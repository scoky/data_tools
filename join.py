#!/usr/bin/python

import sys
import os
import re
import urllib

def test():
	first = True
	items = []
	for v in sys.argv[1:len(sys.argv)]:
		f = open(v, "r")
		i = 0
		for line in f:
			if first:
				items.append(line.rstrip())
			else:
				items[i] += " "+line.rstrip()
				i += 1
		first = False
		f.close()

	for item in items:
		print item
test()

