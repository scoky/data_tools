#!/usr/bin/python

import sys
import os
import re
import urllib

def test():
	dict = {}
	index = int(sys.argv[1])
	while 1:
                line = sys.stdin.readline()
                if not line:
                        break

		chunks = line.rstrip().split()
		key = chunks[index]
		del chunks[index]
		if key not in dict:
			dict[key] = [[], 0]
		dict[key][0].extend(chunks)
		dict[key][1] += 1

	for key in dict.keys():
		print dict[key][1], key, " ".join(dict[key][0])
test()

