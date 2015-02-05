#!/usr/bin/python

import os
import sys
import logging
import argparse
import traceback
from decimal import Decimal
from input_handling import findNumber
from command import Command
import scipy.stats

class FitCommand(Command):
  def __init__(self, dist='norm'):
    super(FitCommand, self).__init__([], self.def_on_row, self.def_on_finish)
    self.dist = getattr(scipy.stats, dist)

  def def_on_row(self, g, lst, val):
    lst.append(findNumber(val))
    return lst

  def def_on_finish(self, g, lst):
    return ' '.join(map(str, self.dist.fit(map(float,lst)))) + ' ' + ' '.join(map(str,scipy.stats.kstest(map(float, lst), self.dist.cdf)))

def fitFile(infile, outfile, col=0, dist='norm', delimiter=None):
    rows = []
    comm = FitCommand(dist)
    for line in infile:
        try:
    	   chunks = line.rstrip().split(delimiter)
	   comm.on_row(None, rows, findNumber(chunks[col]))
	except Exception as e:
           logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())
    outfile.write(comm.on_finish(None, rows)+'\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the distribution fit to column in the input')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-i', '--dist', default='norm')
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

    fitFile(args.infile, args.outfile, args.column, args.dist, args.delimiter)

