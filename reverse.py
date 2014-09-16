#!/usr/bin/python

import sys
import os
import re
import math
import dns_util

def test():
	lines = []

	f = open(sys.argv[1], "r")
	for line in f:
		lines.append(line.rstrip())

	lines.reverse()
	for line in lines:
		print line
test()

