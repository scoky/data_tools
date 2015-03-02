#!/usr/bin/python

import os
import sys
import logging
import argparse
import traceback
from input_handling import findNumber

def compareIn(infile, outfile, columns, elements, testIn=True, delimiter=None):
    jdelim = delimiter if delimiter else ' '
    for line in infile:
        try:
            chunks = line.rstrip().split(delimiter)
            c = jdelim.join([chunks[i] for i in columns])
            if (testIn and c in elements) or (not testIn and c not in elements):
                outfile.write(line)
        except Exception as e:
            logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())

def main():
    elements = set(args.list)
    if args.listfiles:
        for listfile in args.listfiles:
            with open(listfile, 'r') as f:
                for line in f:
                    elements.add(line.rstrip())


compareIn(args.infile, args.outfile, args.columns, elements, not args.notin, args.delimiter)

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Output rows where column(s) is in list')
    parser.add_argument('list', nargs='*', help='List of elements')
    parser.add_argument('-l', '--listfiles', nargs='+', help='Files containing list elements, one per line.')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-n', '--notin', action='store_true', default=False)
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


