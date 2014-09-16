#!/usr/bin/python

import sys
import os

def test():
	lines = []
	for v in sys.argv[1:len(sys.argv)]:
	        f = open(v, "r")
		x = 0
	        for line in f:
			if len(lines) > x:
				lines[x] += " " + line.rstrip()
			else:
				lines.append(line.rstrip())
			x += 1
		f.close()
	for line in lines:
		print line

test()

