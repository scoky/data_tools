#!/usr/bin/python

import sys
import os
sys.path.append(os.path.abspath("/home/kgs7/tools"))
import dns_util
import operator
import math

def test():
	items = set()
	f = open(sys.argv[1], "r")
	index = int(sys.argv[2])
        for line in f:
                items.add(line.rstrip().split()[index])
	f.close()

	index = int(sys.argv[3])
        while 1:
           	next = sys.stdin.readline()
       	        if not next:
			break
                chunks = next.rstrip().split()
		if chunks[index] in items:
			print next.rstrip()

test()


