#!/usr/bin/python

import sys
import os

def test():
	sum = 0
	index = int(sys.argv[1])
#        f = open(sys.argv[2], "r")
        for line in sys.stdin:
	  try:
		chunk = float(line.split()[index].rstrip())
		sum += chunk
	  except:
		e = 1

#	f.close()
	print sum
		

test()

