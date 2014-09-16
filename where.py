#!/usr/bin/python

import sys
import os
import re
import urllib
from decimal import *

def test():
	items = set()
	index = int(sys.argv[1])
	cmd = sys.argv[2]
	type = sys.argv[3]
	if type == "index":
		i2 = int(sys.argv[4])
	else:
		val = Decimal(sys.argv[3])

	while 1:
	  try:
		line = sys.stdin.readline()
                if not line:
                        break

		chunks = line.rstrip().split()
		chunk = Decimal(chunks[index])
		if type == "index":
			val = Decimal(chunks[i2])
		if cmd == ">" and chunk > val:
			print line.rstrip()
		elif cmd == "<" and chunk < val:
			print line.rstrip()
		elif cmd == "=" and chunk == val:
			print line.rstrip()
	  except:
		cept = 1


test()

