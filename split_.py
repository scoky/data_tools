#!/usr/bin/python

import sys
import os
import re
import urllib
from decimal import *

def test():
	items = set()
	index = int(sys.argv[1])
	c = sys.argv[2]
	count = Decimal(sys.argv[3])
	rev = sys.argv[4]

	while 1:
	  try:
		line = sys.stdin.readline()
                if not line:
                        break

		chunk = line.split()[index].rstrip()
		if rev == "r":
			chunks = chunk.rsplit(c, count)
		else:
			chunks = chunk.split(c, count)
		print " ".join(chunks)
	  except:
		cept = 1


test()

