#!/usr/bin/python

import sys
import os
import dns_util

def test():
	index = int(sys.argv[1])
#        f = open(sys.argv[2], "r")
#        for line in f:
	while 1:
	  try:
		line = sys.stdin.readline()
                if not line:
                        break

		chunks = line.rstrip().split()
		chunks[index] = dns_util.IPtoString(int(chunks[index]))
		print " ".join(chunks)
	  except:
		cept = 1

#	f.close()		

test()

