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
	val = Decimal(sys.argv[3])
	rep = Decimal(sys.argv[4])

	while 1:
	  try:
		line = sys.stdin.readline()
                if not line:
                        break

		chunk = Decimal(line.split()[index].rstrip())
		if cmd == ">" and chunk > val:
			chunk = rep
		elif cmd == "<" and chunk < val:
			chunk = rep
		elif cmd == "=" and chunk == val:
			chunk = rep
		print chunk
	  except:
		cept = 1


test()

