#!/usr/bin/python

import sys
import os
from decimal import *
from numpy import dot
from numpy.linalg import norm

def test():
	a = []
	b = []
	i1 = int(sys.argv[1])
	i2 = int(sys.argv[2])
	while 1:
		line = sys.stdin.readline()
                if not line:
                        break

		chunk = line.rstrip().split()
		a.append(Decimal(chunk[i1]))
		b.append(Decimal(chunk[i2]))


	print Decimal(dot(a,b) / (norm(a)*norm(b)))	
test()

