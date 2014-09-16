#!/usr/bin/python

import sys
import os
import random

def test():
	items = set()
	mean_i = int(sys.argv[1])
	stddev_i = int(sys.argv[2])
	samples_i = int(sys.argv[3])

	random.seed()
	while 1:
		line = sys.stdin.readline()
                if not line:
                        break

		chunks = line.rstrip().split()
		mean = float(chunks[mean_i])
		stddev = float(chunks[stddev_i])
		samples = int(chunks[samples_i])

		while samples > 0:
			samples = samples - 1

			print random.gauss(mean, stddev)

test()

