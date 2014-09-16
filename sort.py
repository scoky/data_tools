#!/usr/bin/python

import sys
import os
import re
import math
import dns_util
from decimal import *

def test():
	index = int(sys.argv[1])
	t = sys.argv[2]
	lines = []
        while 1:
                line = sys.stdin.readline()
                if not line:
                        break
		lines.append(line.rstrip().split())

	s = sorted(lines, key=lambda line: int(line[index]) if t == "int" else (Decimal(line[index]) if t == "decimal" else line[index]))
	for line in s:
		print " ".join(line)
test()

