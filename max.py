#!/usr/bin/python

import sys
import os
from decimal import *

def test():
	max = Decimal('0')
	index = int(sys.argv[1])
#        f = open(sys.argv[2], "r")
        for line in sys.stdin:
		try:
			chunk = Decimal(line.split()[index].rstrip())
			if chunk > max:
				max = chunk
		except:
			e = 1

#	f.close()
	print max
		

test()

