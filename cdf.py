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

def cdfFile(infile, keys=0, values=1, delimiter=None):
    total = Decimal(0)
    for line in infile:
        try:
            chunks = line.rstrip().split(delimiter)
            total += findNumber(chunks[values])
            yield [chunks[keys], total]
        except Exception as e:
            logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute cdf from pdf')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-k', '--keys', type=int, default=0)
    parser.add_argument('-a', '--values', type=int, default=1)
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()

    jdelim = args.delimiter if args.delimiter != None else ' '
    for key,value in cdfFile(args.infile, keys=args.keys, values=args.values, delimiter=args.delimiter):
        args.outfile.write(key + jdelim + str(value) + '\n')

