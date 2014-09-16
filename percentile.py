#!/usr/bin/python

import sys
import os
from math import sqrt
from math import pow

def test():
	cur = None
	colRow = sys.argv[1]
	ptile = int(sys.argv[2])
	index = int(sys.argv[3]) # starting index for row, col otherwise

	x = []
	while 1:
                line = sys.stdin.readline()
                if not line:
                        break

		chunks = line.rstrip().split()
		if colRow == "row":
			vals = chunks[index:len(chunks)]
			x = []
			for v in vals:
				x.append(float(v))
			x = sorted(x)
			tile = x[int(len(x)*(float(ptile)/100.0))]
			print " ".join(chunks[0:index]), tile
		else:
			x.append(float(chunks[index]))

	if colRow == "col":
		x = sorted(x)
        	tile = x[int(len(x)*(float(ptile)/100.0))]
	        print tile

test()

