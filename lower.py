#!/usr/bin/python

import sys
import os
import re
import urllib

def test():
	items = set()
	while 1:
	  try:
		line = sys.stdin.readline()
                if not line:
                        break
		print line.lower()
	  except:
		cept = 1


test()

