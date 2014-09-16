#!/usr/bin/python

import sys
import os

def test():
	m = float("inf")
	index = int(sys.argv[1])
        f = open(sys.argv[2], "r")
        for line in f:
		try:
			chunk = int(line.split(" ")[index].rstrip())
			if chunk < m:
				m = chunk
		except:
			e = 1

	f.close()
	print m
		

test()

