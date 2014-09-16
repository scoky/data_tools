#!/usr/bin/python

import sys
import os
import re
import dns_util

def test():
	result = set()
	first = 1
	i = 1
	while i+1 < len(sys.argv):
		index = int(sys.argv[i])
                f = open(sys.argv[i+1], "r")
		temp = set()
                for line in f:
			temp.add(line.rstrip().split()[index])
		i += 2
		if first:
			result = temp
			first  = 0
		else:
			result = result.difference(temp)

	for t in result:
		print t

test()

