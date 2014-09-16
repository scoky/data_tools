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
	accuracy = Decimal(sys.argv[4])
#        f = open(sys.argv[2], "r")
#        for line in f:
	while 1:
#	  try:
		line = sys.stdin.readline()
                if not line:
                        break

		chunk = Decimal(line.split()[index].rstrip()).quantize(accuracy)
		if type == "int":
                        i = int(chunk)
                elif type == "float":
                        i = float(chunk)
		else:
                        i = Decimal(chunk)

		if i not in items:
			items[i] = 0
		items[i] += 1
		total += 1
#	  except:
#		cept = 1

#	f.close()

	arr = []
	for item in items.keys():
		arr.append([item, Decimal(items[item])/Decimal(total)])

	if sort == "key":
		arr = sorted(arr, key=lambda x: x[0])
	elif sort == "value":
		arr = sorted(arr, key=lambda x: x[1])
	for p in arr:
		print p[0], p[1]

test()

