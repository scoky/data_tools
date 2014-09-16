#!/usr/bin/python

import sys
import os
import re
import urllib
from decimal import *

def test():
#        f = open(sys.argv[2], "r")
#        for line in f:
	total = 0
	first = True
	while 1:
#	  try:
		line = sys.stdin.readline()
                if not line:
                        break

		chunks = line.rstrip().split()
		if len(chunks) == 2:
			total += Decimal(chunks[1])
			print chunks[0], total
		elif len(chunks) == 1:
			total += Decimal(chunks[0])
			print total
#	  except:
#		cept = 1

#	f.close()

test()

