#!/usr/bin/python

import sys
import os
from decimal import  *

def test():
	index = int(sys.argv[1])
	index2 = int(sys.argv[2])
#        f = open(sys.argv[2], "r")
#        for line in f:
	while 1:
                line = sys.stdin.readline()
                if not line:
                        break
		chunks = line.rstrip().split()
		print Decimal(chunks[index]) - Decimal(chunks[index2])

#	f.close()
		

test()

