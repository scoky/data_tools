#!/usr/bin/python

import os
import sys
import logging
import argparse
import traceback
from input_handling import parseLines
from decimal import Decimal

class MedianCommand(object):
  def __init__(self, cols):
    self.rows = [[] for i in range(cols)]

  def on_row(self, row):
    map(self.append, self.rows, row)

  def append(self, val1, val2):
    return val1.append(val2)

  def on_finish(self):
    return map(self.median, self.rows)

  def median(self, val1):
    return sorted(val1)[len(val1)/2]

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute mean of column(s)')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
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

    medianc = MedianCommand(len(args.columns))
    for out in parseLines(args.infile, delimiter=args.delimiter, columns=args.columns):
      medianc.on_row(out)
    jdelim = args.delimiter if args.delimiter != None else ' '
    args.outfile.write(jdelim.join(map(str, medianc.on_finish()))+'\n')
