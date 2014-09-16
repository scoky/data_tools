#!/usr/bin/python

import sys
import os

def test():
	items = []
	index = int(sys.argv[1])
#        f = open(sys.argv[2], "r")
#        for line in f:
	while 1:
                line = sys.stdin.readline()
                if not line:
                        break

		chunk = float(line.split()[index].rstrip())
		items.append(chunk)

#	f.close()
	items =  sorted(items)
	print items[len(items)/2]
		

test()

