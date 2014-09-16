#!/usr/bin/python

import sys
import os
import re
import urllib

def test():
	items = set()
	index = int(sys.argv[1])
#        f = open(sys.argv[2], "r")
#        for line in f:
	while 1:
	  try:
		line = sys.stdin.readline()
                if not line:
                        break

		chunk = line.split()[index].rstrip().split(":")[0]
		items.add(chunk)
	  except:
		cept = 1

#	f.close()

	for chunk in items:
		print chunk
		

test()

