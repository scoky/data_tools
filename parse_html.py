#!/usr/bin/python

import sys
import os
import re
import struct

def test():
#	server = re.compile("Server:([^\n]+)")
	manufacture = []
#	manufacture.append(["authenticate:([^\n]+)"])
	manufacture.append(['d-?link', 'dcs-?\d\d', 'dsl-?\d\d\d\d?[a-z]'])
	manufacture.append(['huawei', 'smartax', 'echolife', 'hg\d\d', 'mt\d\d'])
	manufacture.append(['netgear', 'dm\d\d', 'wnr\d\d'])
	manufacture.append(['netcomm', 'nb\d'])
	manufacture.append(['asus', 'rt-[a-z]\d', 'wl-?\d\d'])
	manufacture.append(['belkin', 'e\d[a-z]\d\d', 'f\d[a-z]\d\d'])
	manufacture.append(['buffalo', 'n\d\d\d'])
	manufacture.append(['sapido', 'mb-\d\d\d\d', 'rb-\d\d\d\d', 'gr-\d\d\d\d'])
	manufacture.append(['yamaha'])
	manufacture.append(['tp-?link', 'td-?[a-z]?\d\d\d\d?[a-z]'])
	manufacture.append(['zultrax', 'zxv\d\d'])
	manufacture.append(['zyxel', 'zte', 'nbg\d\d\d', 'mwr\d\d\d'])
	manufacture.append(['cisco'])
	manufacture.append(['iis'])
	manufacture.append(['apache'])
	manufacture.append(['google', 'gws'])
	manufacture.append(['linksys', 'wrt\d\d', 'spa\d\d', 'ea?\d\d\d\d'])
	manufacture.append(['mini_httpd'])
	manufacture.append(['micro_httpd'])
	manufacture.append(['rompager'])

	dict = {}	
	dict["unknown"] = [0, set()]
	for brand in manufacture:
		dict[brand[0]] = [0, set()]

	not_word = '[^a-z0-9]'
	index = int(sys.argv[1])
#        f = open(sys.argv[1], "r")
#        for line in f:
	while 1:
                next = sys.stdin.readline()
                if not next:
                        break
                chunks = next.rstrip().split()
		html = chunks[index].decode('hex').split("\n\n")[0].lower()
		found = 0
		for brand in manufacture:
			for match in brand:
				s = re.compile(not_word+match+not_word)
				m = s.search(html)
				if m:
					dict[brand[0]][0] += 1
					dict[brand[0]][1].add(m.group(0))						
#					print "%s %s" %(ip, brand[0])
#					if brand[0] not in dict:
#						dict[brand[0]] = 0
#					dict[brand[0]] += 1
					found = 1
					break
			if found:
				break
		if not found:
			dict["unknown"][0] += 1
#	f.close()

	keys = sorted(dict.keys())
	for key in keys:
		print "%s %s %s" %(key, dict[key][0], " ".join(dict[key][1]))

test()

