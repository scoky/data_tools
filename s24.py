#!/usr/bin/python

import sys
import os
import re
import urllib
import dns_util

def test():
	items = set()
	index = int(sys.argv[1])
#        f = open(sys.argv[2], "r")
#        for line in f:
	while 1:
		line = sys.stdin.readline()
                if not line:
                        break

		chunk = dns_util.IPfromString(line.split()[index].rstrip()) & 0xffffff00
		items.add(chunk)

#	f.close()

	for chunk in items:
		print dns_util.IPtoString(chunk)
		

test()

