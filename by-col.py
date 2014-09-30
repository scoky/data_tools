#!/usr/bin/python

import logging
import argparse
import sys
import traceback
import os

def by_col(infile, outfile, op, delimiter):
    cols = []
    row = 0
    for line in infile:
        try:
	    chunks = line.rstrip().split(delimiter)
	    while len(chunks) > len(cols):
		cols.append([])
	    for i in range(len(cols)):
		while len(cols[i]) < row:
			cols[i].append(None)
		if len(chunks) > i:
			cols[i].append(chunks[i])
		else:
			cols[i].append(None)
	    row += 1
	except Exception as e:
            logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())

    for col in cols:
	outfile.write(op(col))

def main():
    by_col(args.infile, args.outfile, eval(args.operation), args.delimiter)

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Perform an operation upon each column.')
    parser.add_argument('operation', help='lambda expression that takes a single argument column as array.')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
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

    main()


