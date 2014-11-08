#!/usr/bin/python

import os
import sys
import logging
import argparse
import traceback
import operator
from decimal import Decimal,getcontext
from input_handling import findNumber,parseLines
from collections import defaultdict

def pdfFile(infile, outfile, column=0, quantize=None, sigDigits=None, binColumn=None, delimiter=None, order='key', padding=[]):
  if len(padding) % 2 != 0:
    raise Exception('Invalid padding!')

  # Set precision
  if sigDigits:
    getcontext().prec = sigDigits

  # Quantize input
  if quantize:
    getFunc = lambda cols: findNumber(cols[column]).quantize(quantize)
  else:
    getFunc = lambda cols: findNumber(cols[column])

  # Input is binned
  if binColumn:
    addFunc = lambda cols: findNumber(cols[binColumn])
  else:
    addFunc = lambda cols: Decimal(1)

  jdelim = delimiter if delimiter != None else ' '

  bins = defaultdict(Decimal)
  total = Decimal(0)

  for line in infile:
    try:
      chunks = line.rstrip().split(delimiter)
      value = getFunc(chunks)
      count = addFunc(chunks)
      bins[value] += count
      total += count
    except Exception as e:
      logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())

  # Insert padding
  i = 0
  while i+1 < len(padding):
    bins[padding[i]] += padding[i+1]
    total += padding[i+1]
    i += 2

  for key in bins:
    bins[key] = bins[key]/total

  sort_bins = sorted(bins.items(), key=operator.itemgetter(0 if order=='key' else 1))
  for pair in sort_bins:
    outfile.write(jdelim.join(map(str, pair))+'\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute pdf')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0, help='column contain values')
    parser.add_argument('-b', '--bin', type=int, default=None, help='column containing bin counts')
    parser.add_argument('-u', '--quantize', type=Decimal, default=None, help='fixed exponent')
    parser.add_argument('-s', '--significantDigits', type=int, default=None, help='number of significant digits')
    parser.add_argument('-d', '--delimiter', default=None, help='delimiter between columns in file')
    parser.add_argument('-r', '--order', choices=['key', 'value'], default='key', help='sort order of the output')
    parser.add_argument('-p', '--padding', nargs='+', type=Decimal, default=[], help='additional binned values to add. format: "value count"')
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

    pdfFile(args.infile, args.outfile, column=args.column, quantize=args.quantize, sigDigits=args.significantDigits,\
       binColumn=args.bin, delimiter=args.delimiter, order=args.order, padding=args.padding)


