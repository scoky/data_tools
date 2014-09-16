#!/usr/bin/python

import sys
import os
import re
import urllib

def test():
	items = set()
	ordered = []
	index = int(sys.argv[1])
#        f = open(sys.argv[2], "r")
#        for line in f:
	while 1:
	  try:
		line = sys.stdin.readline()
                if not line:
                        break

		chunk = line.split()[index].rstrip().split(":")[0]
		if chunk not in items:
			items.add(chunk)
			ordered.append(chunk)
	  except:
		cept = 1

#	f.close()

	for chunk in ordered:
		print chunk
		

test()

