#!/usr/bin/python

import logging
import argparse
import sys
import traceback
import os

def formset(infile, outfile, index, delimiter):
    items = set()
    for line in infile:
        try:
    	   chunk = line.split(delimiter)[index].rstrip()
	   if chunk not in items:
	      items.add(chunk)
	      outfile.write(chunk+'\n')
	except Exception as e:
           logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())

def main():
    formset(args.infile, args.outfile, args.column, args.delimiter)

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the set of strings from a column in files.')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
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

