#!/usr/bin/python

import sys
import os
import re
import socket
import math
from traceback import *
from dnslib import *

def time_delta(x, y):
	return int(math.ceil(float(x-y) / 1000.0))

def rough_equiv(ttl, report, range):
        if abs(report - ttl) <= range:
                return 1
        return 0

def loadFile(s):
	r = []
	f = open(s, "r")
	for line in f:
		r.append(line.rstrip())
	return r

def saveFile(r, s):
	f = open(s, "w")
	for line in r:
		f.write("%s\n" %line)
	f.close()

class QueryString:
	odns = None
	rdns = None
	query_id = None
	seq_id = None
	cname_id = None
	ttl = None
	expt = None

def processMPLine(line):
        words = line.split(' ')
        if len(words) > 4 and words[2] == "QUERY:":
                time = long(words[3])
		qs = parseQueryString(words[4])
                return time, qs.odns, qs.query_id, qs.seq_id
        return -1, -1, -1, -1

def processADNSLine(line):
        words = line.split(' ')
        parsed = "";
        if len(words) > 2 and words[1] == "Received":
        	time = long(words[0])
        	rdns = words[4].split(':')[0]        	
                
                for i in range(len(words)):
                	if words[i] == "contents:":
                		r = DNSRecord.parse(words[i+1].rstrip().decode('hex'))
                		return time, rdns, str(r.get_q().qname)
        return -1, -1, -1

def parseDnsQuery(encoded):
	r = DNSRecord.parse(encoded.decode('hex'))
	return str(r.get_q().qname)

def get_conn():
	return MySQLdb.connect(host = "localhost", user = "root", passwd = "x.1223.y", db = "scan_db")


def nextADNSLine():
	next = ""
	while 1:
		try:
			next = sys.stdin.readline()
                	if not next:
				break
        	        time, rdns, qs = processADNSLine(next)
			qs = parseQueryString(qs)
			if time != -1:
				return time, rdns, qs.odns, qs.query_id, qs.seq_id, qs.cname_id
		except:
			sys.stderr.write("Error %s on: %s\n" %(str(sys.exc_info()), next.rstrip()))
       	return -1, -1, -1, -1, -1, -1

def nextADNS():
	next = ""
        while 1:
                try:
                        next = sys.stdin.readline()
                        if not next:
                                break
                        time, rdns, qs = processADNSLine(next)
                        if time != -1:
				return time, rdns, qs
		except:
			sys.stderr.write("Error %s on: %s\n" %(str(sys.exc_info()), next.rstrip()))
        return -1, -1, -1

def nextChainLine(expt):
	next = ""
        while 1:
                try:
                        next = sys.stdin.readline()
                        if not next:
                                break
			words = next.rstrip().split()
		        parsed = ""
		        if len(words) > 2 and words[1] == "Sending":
		                time = long(words[0])
                		rdns = words[4].split(':')[0]

		                for i in range(len(words)):
                        		if words[i] == "contents:":
		                                r = DNSRecord.parse(words[i+1].rstrip().decode('hex'))
						qs1 = str(r.get_q().qname).lower()
						if expt not in qs1:
							continue
						qs2 = str(r.get_a().rdata).lower()
						cname = r.get_a().rtype == QTYPE.CNAME
						return time, rdns, qs1, qs2, cname
                except:
			sys.stderr.write("Error %s on: %s\n" %(str(sys.exc_info()), next.rstrip()))
        return -1, -1, -1, -1, -1


def nextMPLine():
	next = ""
	while 1:
		try:
			next =  sys.stdin.readline()
	                if not next:
        	                break
			time, odns, queryID, seqID = processMPLine(next)
			if time != -1:
				return time, odns, queryID, seqID
		except:
			sys.stderr.write("Error %s on: %s\n" %(str(sys.exc_info()), next.rstrip()))
	return -1, -1, -1, -1

def nextLine():
	next = sys.stdin.readline()
	if not next:
		return -1
	return next.rstrip().split()

def nextMPStudyResult():
	while 1:
		try:
			next = sys.stdin.readline()
			if not next:
				break
			chunks = next.rstrip().split()
			if len(chunks) > 4 and chunks[3] == "STUDY-RESULT:":
				time = long(chunks[2])
				odns = chunks[4].split(":")[0]
				r = DNSRecord.parse(chunks[6].decode('hex'))
				if len(r.rr) > 0:
					return time, odns, r
		except:
			sys.stderr.write("Error %s on: %s\n" %(str(sys.exc_info()), next.rstrip()))
	return -1, -1, -1

def parseQueryString(query):
	qs = QueryString()
	chunks = query.lower().split(".")
	i = 0
	while i < len(chunks):
		if chunks[i].startswith("odns") and i + 3 < len(chunks):
			qs.odns = chunks[i][4:]+"."+chunks[i+1]+"."+chunks[i+2]+"."+chunks[i+3]
			i += 3
		elif chunks[i].startswith("rdns") and i + 3 < len(chunks):
                        qs.rdns = chunks[i][4:]+"."+chunks[i+1]+"."+chunks[i+2]+"."+chunks[i+3]
                        i += 3
		elif chunks[i].startswith("queryid"):
			qs.query_id = long(chunks[i][7:])
		elif chunks[i].startswith("seqid"):
			qs.seq_id = int(chunks[i][5:])
		elif chunks[i].startswith("cname"):
			qs.cname_id = int(chunks[i][5:])
		elif chunks[i].startswith("ttl"):
			qs.ttl = long(chunks[i][3:])			
		elif chunks[i].startswith("expt"):
			qs.expt = chunks[i][4:]
		i += 1
	return qs


def IPfromString(ip):
	return int(socket.inet_aton(ip).encode('hex'),16);
	

def IPtoString(ip):
	return socket.inet_ntoa(struct.pack('!I', ip))
