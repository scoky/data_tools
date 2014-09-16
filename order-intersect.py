#!/usr/bin/python

import sys
import os
import re
import dns_util

def test():
	result = set()
	items = []
	first = 1
	i = 1
	while i + 1 < len(sys.argv):
		index = int(sys.argv[i])
                f = open(sys.argv[i+1], "r")
		temp = set()
                for line in f:
			chunk = line.rstrip().split()[index]
			temp.add(chunk)
			if first:
				items.append(chunk)
		i += 2
		if first:
			result = temp
			first = 0
		else:
			result = result.intersection(temp)

	for t in items:
		if t in result:
			print t

test()

