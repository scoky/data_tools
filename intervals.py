#!/usr/bin/python

import os
import sys
import logging
import argparse
import traceback
from decimal import Decimal
from input_handling import findNumber
from command import Command

class IntervalCommand(Command):
  def __init__(self):
    super(IntervalCommand, self).__init__([None, []], self.def_on_row, self.def_on_finish)

  def def_on_row(self, g, lst, val):
    val=findNumber(val)
    if lst[0] != None:
      lst[1].append(val-lst[0])
    lst[0]=val
    return lst

  def def_on_finish(self, g, lst):
    return ' '.join(map(str, lst[1]))

def intervalFile(infile, outfile, col=0, delimiter=None):
    comm = IntervalCommand()
    rows = comm.init
    for line in infile:
        try:
    	   chunks = line.rstrip().split(delimiter)
	   comm.on_row(None, rows, chunks[col])
	except Exception as e:
           logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())
    for item in rows[1]:
      outfile.write(str(item)+'\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the difference between subsequent elements in a column')
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

    intervalFile(args.infile, args.outfile, args.column, args.delimiter)

