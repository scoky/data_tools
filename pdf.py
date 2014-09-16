#!/usr/bin/python

import sys
import os
import re
import urllib
from decimal import *

def test():
	items = {}
	total = 0
	index = int(sys.argv[1])
	type = sys.argv[2]
	sort = sys.argv[3]
#        f = open(sys.argv[2], "r")
#        for line in f:
	while 1:
#	  try:
		line = sys.stdin.readline()
                if not line:
                        break

		chunk = line.split()[index].rstrip()
		if chunk not in items:
			items[chunk] = 0
		items[chunk] += 1
		total += 1
#	  except:
#		cept = 1

#	f.close()

	arr = []
	for item in items.keys():
		if type == "int":
			i = int(item)
		elif type == "float":
			i = float(item)
		elif type == "decimal":
			i = Decimal(item)
		else:
			i = item
		arr.append([i, Decimal(items[item])/Decimal(total)])

	if sort == "key":
		arr = sorted(arr, key=lambda x: x[0])
	elif sort == "value":
		arr = sorted(arr, key=lambda x: x[1])
	print 0, 0
	for p in arr:
		print p[0], p[1]		

test()

