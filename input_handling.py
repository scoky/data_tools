#!/usr/bin/python

import logging
import argparse
import sys
import traceback
import os
import re
import socket
from decimal import Decimal
from decimal import InvalidOperation

number_pattern = re.compile("(-?\d+\.?\d*(e[\+|\-]?\d+)?)", re.IGNORECASE)
ip_pattern = re.compile("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")

# Search an input value for a number
def findNumber(value):
   try:
     return Decimal(value)
   except InvalidOperation as e:
     return Decimal(number_pattern.search(value).group())

# Search an input value for a number
def findSignificantNumber(value, digits):
   try:
     return Decimal(value)
   except InvalidOperation as e:
     return Decimal(number_pattern.search(value).group())

def findIPAddress(value):
   m = ip_pattern.search(value)
   if m:
	return m.group()
   return socket.gethostbyname(value)

def parseLines(infile, delimiter=None, columns=[0], function=findNumber):
  for line in infile:
     try:
        chunks = line.rstrip().split(delimiter)
	yield [function(chunks[i] for i in columns)]
     except Exception as e:
        logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Parse input base upon available functions')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default='0')
    parser.add_argument('-f', '--function', choices=['findNumber'], default='findNumber')
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
      try:
	chunks = line.rstrip().split(args.delimiter)
	args.outfile.write(jdelim.join([str(args.function(chunks[i])) for i in args.columns])+'\n')
      except Exception as e:
        logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())
    
