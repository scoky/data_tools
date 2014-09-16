#!/usr/bin/python

import sys
import os
import math

def test():
       	lines = []
       	filename = sys.argv[2]
       	count = int(sys.argv[3])
     	f = open(sys.argv[1], "r")
        for line in f:
		lines.append(line.rstrip())

	max = int(math.ceil(float(len(lines)) / float(count)));
	cur = 0
	i = 1
	f = open(filename+"."+str(i), "w")
	for line in lines:
		if cur >= max:
			cur = 0
			i += 1
			f.close()
			f = open(filename+"."+str(i), "w")
		f.write(line+"\n")
		cur += 1

test()

