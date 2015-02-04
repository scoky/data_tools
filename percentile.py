#!/usr/bin/python

import os
import sys
import logging
import argparse
import traceback
from decimal import Decimal
from input_handling import findNumber
from command import Command

DEFAULT_PCT = map(Decimal, [0, 0.01, 0.25, 0.5, 0.75, 0.99, 1])

class PercentileCommand(Command):
  def __init__(self, pts=DEFAULT_PCT):
    super(PercentileCommand, self).__init__([], self.def_on_row, self.def_on_finish)
    self.pts = pts

  def def_on_row(self, g, lst, val):
    lst.append([val, findNumber(val)])
    return lst

  def def_on_finish(self, g, lst):
    return ' '.join(percentile(lst, pts=self.pts, keys=0, values=1))

def percentile(rows, pts=DEFAULT_PCT, keys=0, values=0):
    rows = sorted(rows, key = lambda l: l[values])
    indices = [int(pt*(len(rows)-1)) for pt in pts]
    return [rows[index][keys] for index in indices]

def percentileFile(infile, outfile, pts=DEFAULT_PCT, keys=0, values=0, delimiter=None):
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
    parser.add_argument('-p', '--percentiles', nargs='+', type=Decimal, default=DEFAULT_PCT)
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

