#!/usr/bin/python

from dnslib import *
import sys
import os
from traceback import *





def processLine(line):
	empty = ""
	words = line.split(' ')
	contents = 0
	out = ""
	for word in words:
		word = word.rstrip()
		if contents == 1:
			word = empty.join(word.split("."))
			parsed = str(DNSRecord.parse(word.decode('hex')))
			for entry in parsed.splitlines():
				#if "RR:" in entry:
				out += entry
			out += " "
			contents = 0
		else:
			out += word +" "
			if word == "contents:":
				contents = 1
			else:
				contents = 0
	print out







def test():
        while 1:
                try:
                        next = sys.stdin.readline()
                        if not next:
                                break
			processLine(next)
		except:
			e = 1
#			s = "Error: %s\n" %str(sys.exc_info())
#			sys.stderr.write(s)


test()

