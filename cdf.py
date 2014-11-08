#!/usr/bin/python

import os
import sys
import logging
import argparse
import traceback
from input_handling import findNumber
from decimal import Decimal

def cdf(rows, keys=0, values=1):
    total = Decimal(0)
    for r in rows:  
       total += r[values] 
       yield [r[keys], total]    

def cdfFile(infile, outfile, keys=0, values=1, delimiter=None):
    total = Decimal(0)
    rows = []
    for line in infile:
        try:
    	   chunks = line.rstrip().split(delimiter)
	   rows.append([chunks[keys], findNumber(chunks[values])])
	except Exception as e:
           logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())

    jdelim = delimiter if delimiter != None else ' '
    for val in cdf(rows, keys=0, values=1):
	outfile.write(val[0]+jdelim+str(val[1])+'\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute cdf from pdf')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-k', '--keys', type=int, default=0)
    parser.add_argument('-a', '--values', type=int, default=1)
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help='only print errors')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print debug info. --quiet wins if both are present')
    args = parser.parse_args()

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

    cdfFile(args.infile, args.outfile, keys=args.keys, values=args.values, delimiter=args.delimiter)

