#!/usr/bin/python

import sys
import os
import re
import urllib
from decimal import *

def test():
	index = []
	for v in sys.argv[1:len(sys.argv)]:		
		index.append([abs(int(v)), "-" in v])
#        f = open(sys.argv[2], "r")
#        for line in f:
	while 1:
#	  try:
		line = sys.stdin.readline()
                if not line:
                        break

		chunks = line.rstrip().split()
		t = Decimal('0')
		for v in index:
			if v[1]:
				t = t - Decimal(chunks[v[0]])
			else:
				t = t + Decimal(chunks[v[0]])
		print t
#	  except:
#		cept = 1

#	f.close()

test()

