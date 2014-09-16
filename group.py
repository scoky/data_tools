#!/usr/bin/python

import sys
import os
from math import sqrt
from math import pow

def test():
	cur = None
	gindex = int(sys.argv[1])
	action = sys.argv[2]
	index = int(sys.argv[3])
	max_index = max(index,gindex)

	if action == "max" or action == "mean" or action == "sum" or acount == "count":
		init = 0
	else:
		init = float("inf")
	v = init
	c = 0
	dict = {}
#        f = open(sys.argv[2], "r")
#        for line in f:
	while 1:
                line = sys.stdin.readline()
                if not line:
                        break

		chunks = line.rstrip().split()
		if len(chunks) <= max_index:
			continue

		key = chunks[gindex]
		if key not in dict:
			if action == "set":
				dict[key] = [init, 0, set()]
			else:
				dict[key] = [init, 0, []]
		
#		if cur != chunks[gindex] and cur != None:
#			if action == "mean":
#				print cur, v/c
#			else:
#				print cur, v
#			v = init
#			c = 0

#		c += 1
		dict[key][1] += 1
		if action == "max" and float(chunks[index]) > dict[key][0]:
			dict[key][0] = float(chunks[index])
		if action == "min" and  float(chunks[index]) < dict[key][0]:
			dict[key][0] = float(chunks[index])
		if action == "mean":
			dict[key][0] += float(chunks[index])
			dict[key][2].append(float(chunks[index]))
		if action == "sum":
			dict[key][0] += int(chunks[index])
		if action == "count":
			dict[key][0] += 1
		if action == "set":
			dict[key][2].add(chunks[index])
			
#		cur = chunks[gindex]
		

#	f.close()
	for key in sorted(dict.keys()):
		if action == "mean":
			dict[key][0] = dict[key][0] / dict[key][1]

			# dev
			m = 0
			for v in dict[key][2]:
				m += pow(v - dict[key][0], 2)
			m = sqrt(m / dict[key][1])


			# median
			s = sorted(dict[key][2])
			med = s[len(s)/2]
			up90 = s[int(len(s)*0.95)]
			up50 = s[int(len(s)*0.75)]
			up20 = s[int(len(s)*0.60)]
			down20 = s[int(len(s)*0.40)]
			down50 = s[int(len(s)*0.25)]
			down90 = s[int(len(s)*0.05)]
			print key, dict[key][0], m, down90, down50, down20, med, up20, up50, up90
		elif action == "set":
			print key, len(dict[key][2])
		else:
			print key, dict[key][0]
		
		

test()

