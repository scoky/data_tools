#!/usr/bin/python

import logging
import argparse
import sys
import traceback
import os

def columns(infile, outfile, cols, delimiter):
    jdelim = delimiter if delimiter != None else ' '
    for line in infile:
        try:
	    chunks = line.rstrip().split(delimiter)
	except Exception as e:
            logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())
	    continue
	outfile.write(jdelim.join([chunks[i] for i in cols])+'\n')

def main():
    columns(args.infile, args.outfile, args.columns, args.delimiter)

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Select columns from a table file.')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default='0', help='can specify column indices, or ranges (e.g., 0:4)')
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help='only print errors')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print debug info. --quiet wins if both are present')
    args = parser.parse_args()

    cols = args.columns
    args.columns = []
    for c in cols:
        vals = c.split(':', 1)
        if len(vals) == 1:
            args.columns.append(int(vals[0]))
        elif len(vals) == 2:
            args.columns += range(int(vals[0]), int(vals[1])+1)
        else:
            raise Exception('invalid column parameter')

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


