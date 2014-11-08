#!/usr/bin/python

import os
import sys
import logging
import argparse
import traceback
from decimal import Decimal
from input_handling import findNumber

def percentile(rows, pts=[0, 0.25, 0.5, 0.75, 100], keys=0, values=0):
    maximum = rows[-1][values]
    pt = 0
    for r in rows:       
       while r[values] >= pts[pt]*maximum:
          yield r[keys]
          pt += 1
          if pt >= len(pts):
             break
    while pt < len(pts):
       yield rows[-1][keys]
       pt += 1

def percentileFile(infile, outfile, pts=[0, 0.25, 0.5, 0.75, 100], keys=0, values=0, delimiter=None):
    rows = []
    for line in infile:
        try:
    	   chunks = line.rstrip().split(delimiter)
	   rows.append([chunks[keys], findNumber(chunks[values])])
	except Exception as e:
           logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())
    for val in percentile(rows, pts=pts, keys=0, values=1):
	outfile.write(val+'\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the percentiles of a two column format')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-k', '--keys', type=int, default=0)
    parser.add_argument('-a', '--values', type=int, default=0)
    parser.add_argument('-p', '--percentiles', nargs='+', type=Decimal, default=[0, 0.25, 0.5, 0.75, 100])
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

    percentileFile(args.infile, args.outfile, args.percentiles, args.keys, args.values, args.delimiter)

