#!/usr/bin/python

import os
import sys
import logging
import argparse
import traceback
from input_handling import parseLines,findNumber
from decimal import Decimal

class MinCommand(object):
  def __init__(self, cols):
    self.min = [Decimal('Inf')]*cols

  def on_row(self, row):
    self.min = map(min, self.min, row)

  def on_finish(self):
    return self.min

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute minimum of column(s)')
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

    minc = MinCommand(len(args.columns))
    for out in parseLines(args.infile, delimiter=args.delimiter, columns=args.columns, function=findNumber):
      minc.on_row(out)
    jdelim = args.delimiter if args.delimiter != None else ' '
    args.outfile.write(jdelim.join(map(str, minc.on_finish()))+'\n')
