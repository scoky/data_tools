#!/usr/bin/python

import sys
import os
import re
import urllib
import dns_util

def test():
	items = []
	total = 0
	index = int(sys.argv[1])
	type = sys.argv[2]
	sort = sys.argv[3]
#        f = open(sys.argv[2], "r")
#        for line in f:
	while 1:
	  try:
		line = sys.stdin.readline()
                if not line:
                        break

		chunk = int(line.split()[index].rstrip())
		found = 0
		for i in items:
			if dns_util.rough_equiv(i[0], chunk, 10):
				i[1] += 1
				found = 1
		if not found:
			items.append([chunk, 1])
		total += 1
	  except:
		cept = 1

#	f.close()

	for i in items:
		i[1] = float(i[1])/float(total)

	if sort == "key":
		items = sorted(items, key=lambda x: x[0])
	elif sort == "value":
		items = sorted(items, key=lambda x: x[1])
	for p in items:
		print p[0], p[1]		

test()

