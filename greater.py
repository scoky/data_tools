#!/usr/bin/python

import sys
import os

def test():
	max = 0
	index = int(sys.argv[1])
        f = open(sys.argv[2], "r")
	value  = int(sys.argv[3])
        for line in f:
		try:
			chunk = int(line.split(" ")[index].rstrip())
			if chunk > value:
				max += 1
		except:
			e = 1

	f.close()
	print max
		

test()

