#!/usr/bin/python

import os
import sys
import logging
import argparse
import traceback

def aggregate(infiles, outfile, column=0, delimiter=None):
    jdelim = delimiter if delimiter != None else ' '
    dict = {}
    for infile in infiles:
      for line in infile:
        try:
	    chunks = line.rstrip().split(delimiter)
            key = chunks[column]
            if key not in dict:
               dict[key] = chunks
            else:
               for chunk in chunks:
                  if chunk not in dict[key]:
                    dict[key].append(chunk)
	except Exception as e:
            logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())

    for key in dict:
	outfile.write(jdelim.join(dict[key])+'\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Aggregate 2 or more files')
    parser.add_argument('infiles', nargs='+', type=argparse.FileType('r'))
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

    aggregate(args.infiles, args.outfile, column=args.column, delimiter=args.delimiter)

