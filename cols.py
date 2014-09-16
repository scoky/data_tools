#!/usr/bin/python

import sys
import os
import re
import urllib

def test():
	items = set()
	index = []
	for v in sys.argv[1:len(sys.argv)]:
		index.append(int(v))
#        f = open(sys.argv[2], "r")
#        for line in f:
	while 1:
#	  try:
		line = sys.stdin.readline()
                if not line:
                        break

		chunk = line.rstrip().split()
		print " ".join([chunk[i] for i in index])
#	  except:
#		cept = 1

#	f.close()

test()

