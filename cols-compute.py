#!/usr/bin/python

import logging
import argparse
import sys
import traceback
import os
import re
from input_handling import findNumber

def compute(infile, outfile, expression):
    # Pattern to pull out integers which represent columns
    pattern = re.compile("(\d+)")
    # Replace integers with indices into an array and convert to a lambda expression
    expression = eval('lambda c: '+ pattern.sub(r'findNumber(c[\1])', args.expression))
    for line in infile:
        chunks = line.rstrip().split()
        try:    
	    # Evaluate lambda with the row input from the file
	    outfile.write('%s\n' % expression(chunks))
    	except Exception as e:
            logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())

def main():
    compute(args.infile, args.outfile, args.expression)

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the set of strings from a column in files.')
    parser.add_argument('expression')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
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

    main()

