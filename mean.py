#!/usr/bin/python

import sys
import os

def test():
	sum = 0
	count = 0
	index = int(sys.argv[1])
#        f = open(sys.argv[2], "r")
#        for line in f:
	while 1:
                line = sys.stdin.readline()
                if not line:
                        break

		chunk = float(line.split()[index].rstrip())
		sum += chunk
		count += 1

#	f.close()
	print float(sum)/float(count)
		

test()

