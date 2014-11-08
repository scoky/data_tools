#!/usr/bin/python

import os
import sys
import logging
import argparse
import traceback
from input_handling import parseLines
from decimal import Decimal

class MeanCommand(object):
  def __init__(self, cols):
    self.total = [0]*cols
    self.count = 0

  def on_row(self, row):
    self.total = map(self.add, self.total, row)
    self.count += 1

  def add(self, val1, val2):
    return val1+val2

  def on_finish(self):
    return map(self.divide, self.total)

  def divide(self, val1):
    return val1/self.count

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

    meanc = MeanCommand(len(args.columns))
    for out in parseLines(args.infile, delimiter=args.delimiter, columns=args.columns):
      meanc.on_row(out)
    jdelim = args.delimiter if args.delimiter != None else ' '
    args.outfile.write(jdelim.join(map(str, meanc.on_finish()))+'\n')
