#!/usr/bin/python

import sys
import os
import re
import dns_util

def test():
	result = set()
	i = 1
	while i < len(sys.argv):
                f = open(sys.argv[i], "r")
		temp = set()
                for line in f:
			temp.add(line.rstrip())
		i += 1
		result = result.union(temp)

	for t in result:
		print t

test()

