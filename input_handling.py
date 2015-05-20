#!/usr/bin/python

import logging
import argparse
import sys
import traceback
import os
import re
import socket
import glob
import datetime
import struct
from decimal import Decimal
from decimal import InvalidOperation

number_pattern = re.compile("(-?\d+\.?\d*(e[\+|\-]?\d+)?)", re.IGNORECASE)
ip_pattern = re.compile("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")

def findIdentity(value):
    return value

def findFloat(value):
    return float(value)

def findInt(value):
    return int(value)

# Search an input value for a number
def findNumber(value):
    try:
        return Decimal(value)
    except InvalidOperation:
        return Decimal(number_pattern.search(value).group())

# Search an input value for a number
def findSignificantNumber(value, digits):
    try:
        return Decimal(value)
    except InvalidOperation:
        return Decimal(number_pattern.search(value).group())

def findIPAddress(value):
    try:
        # Might be a simple integer
        return int(value)
    except ValueError:
        m = ip_pattern.search(value)
        if m: # IP address in octet notation
	        return IPfromString(m.group())
        else: # Potentially a hostname
            return socket.gethostbyname(value)

def IPfromString(ip):
    return struct.unpack("!I", socket.inet_aton(ip))[0]

def IPtoString(ip):
    return socket.inet_ntoa(struct.pack("!I", int(ip)))

def MACfromString(mac):
    return int(mac.replace(':', ''), 16)

def MACtoString(mac):
    mac = hex(int(mac)).lstrip('0x')
    mac = '0'*(12-len(mac))+mac
    return ':'.join([mac[i:i+2] for i in xrange(0, len(mac), 2)])

def ToUnixTime(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.days*86400 + delta.seconds

def ToDateTime(dt):
    return datetime.datetime.utcfromtimestamp(dt)

def parseLines(infile, delimiter=None, columns=[0], function=findIdentity):
    for line in infile:
        try:
            chunks = line.rstrip().split(delimiter)
            yield [function(chunks[i]) for i in columns]
        except IndexError as e:
            logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())

def concatFiles(files, opts='r'):
    for f in files:
        for line in openFile(f, opts):
            yield line

def fileRange(startFile, endFile):
    startDir, startFile = os.path.split(startFile)
    _, endFile = os.path.split(endFile)
    if startDir == '':
        files = glob.iglob('*');
    else:
        files = glob.iglob(startDir + '/*');
    ret = []
    for fn in files:
        if os.path.basename(fn) >= startFile and os.path.basename(fn) <= endFile:
            ret.append(fn)
    return sorted(ret)

def openFile(filename, opts):
    return gzip.open(filename, opts+'b') if filename.endswith('.gz') else open(filename, opts)

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Parse input base upon available functions')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    parser.add_argument('-f', '--function', choices=['IPtoString', 'IPfromString', 'MACtoString', 'MACfromString', 'findNumber', 'findIPAddress'], default='findNumber')
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help='only print errors')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print debug info. --quiet wins if both are present')
    args = parser.parse_args()
    args.function = getattr(sys.modules[__name__], args.function)

    # set up logging
    if args.quiet:
        level = logging.WARNING
    elif args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(
        format = "%(levelname) -10s %(asctime)s %(module)s:%(lineno) -7s %(message)s",
        level = level
    )

    jdelim = args.delimiter if args.delimiter != None else ' '
    for line in args.infile:
        chunks = line.rstrip().split(args.delimiter)
        vals = [args.function(chunks[i]) for i in args.columns]
        if args.append:
            args.outfile.write('%s%s' % (line.rstrip(), jdelim))
        args.outfile.write(jdelim.join(map(str,vals))+'\n')
    
