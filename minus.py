#!/usr/bin/python

import sys
import os

def test():
	while 1:
                line = sys.stdin.readline()
                if not line:
                        break

		chunks = line.rstrip().split()
		v1 = int(chunks[2])
		v2 = int(chunks[3])
		if v1 != -1 and v2 != -1:
			d = v2 - v1
			if d < 0:
				d = 0
			print chunks[0], chunks[1], d
		

test()

