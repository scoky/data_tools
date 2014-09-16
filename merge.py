#!/usr/bin/python

import sys
import os

def test():
	dict = {}
	i = 1
	first = True
	while i+1 < len(sys.argv):
	        f = open(sys.argv[i], "r")
		index = int(sys.argv[i+1])
		for line in f:
			chunks = line.rstrip().split()
			key = chunks[index]
			del chunks[index]
		
			if first:			
#				key = key+"."
				dict[key] = [1] + chunks
			elif key in dict:
				dict[key] += chunks
				dict[key][0] += 1
		first = False
		f.close()
		i += 2
	files = (i-1) / 2

	for key in dict.keys():
		if dict[key][0] == files:
			print key, " ".join(dict[key][1:len(dict[key])])

test()

