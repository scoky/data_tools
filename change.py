#!/usr/bin/python

import sys
import os
import re
import urllib

def test():
	item = None
	c = 0
	index = int(sys.argv[1])
#        f = open(sys.argv[2], "r")
#        for line in f:
	while 1:
#	  try:
		line = sys.stdin.readline()
                if not line:
                        break

		chunk = line.split()[index].rstrip()
		if item != chunk:
			item = chunk
			c += 1
			print chunk
#	  except:
#		cept = 1

#	f.close()
	print c

test()

