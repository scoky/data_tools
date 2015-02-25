#!/usr/bin/python

import os
import re
import sys
import logging
import argparse
import traceback
from input_handling import findNumber
from decimal import Decimal

def compare(infile, outfile, statement, delimiter):
	for line in infile:
	    try:
            c = line.rstrip().split(delimiter)
            if eval(statement):
                outfile.write(line)
        except Exception as e:
            logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Output rows where comparator is true')
    parser.add_argument('statement', default='c[0]>0', help='boolean statement to evaluate. use c[i] to indicate column i')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-f', '--findNumber', action='store_true', default=False, help='find number in column values')
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help='only print errors')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print debug info. --quiet wins if both are present')
    args = parser.parse_args()
    if args.findNumber:
        pattern = re.compile('(c\[\d+\])')
        args.statement = pattern.sub(r'findNumber(\1)', args.statement)

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

    compare(args.infile, args.outfile, args.statement, args.delimiter)

