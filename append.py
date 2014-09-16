#!/usr/bin/python

import sys
import os
import re
import urllib

def test():
	count = int(sys.argv[1])
	toa = sys.argv[2]
	while count > 0:
		print toa
		count -= 1		

test()

