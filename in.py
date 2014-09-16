#!/usr/bin/python

import sys
import os

def test():
	dict = set()
	i = 1
	IN = True
	if sys.argv[i] == "not":
		IN = False
		i += 1
	first = True
	while i+1 < len(sys.argv):
	        f = open(sys.argv[i], "r")
		index = int(sys.argv[i+1])
		for line in f:
			chunks = line.rstrip().split()
			key = chunks[index]
		
			if first:			
				dict.add(key)
			elif (IN and key in dict) or (not IN and key not in dict):
				print line.rstrip()
		first = False
		f.close()
		i += 2

test()

