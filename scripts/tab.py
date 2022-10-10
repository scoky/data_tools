#!/usr/bin/env python

import os
import sys
from data_tools.files import ParameterParser

def printCols(data, headers = None, stream = sys.stdout, min_lengths = None, precision = None):
   rows = []
   if headers is not None:
      rows.append(headers)
   rows.extend(data)
   # Nothing to print!
   if len(rows) == 0:
      return None

   # Set the initial lengths
   lengths = min_lengths if min_lengths is not None else [0] * len(rows[0])
   # Update precision of floats
   if not precision is None:
      newRows = []
      for row in rows:
         row = [('{:.' + str(precision) + 'f}').format(float(v)) if isFloatingPoint(v) else v for v in row]
         newRows.append(row)
      rows = newRows
   # Run once over the rows to find the maximum column lengths
   for row in rows:
      lengths = [max(lengths[c], len(v)) for c,v in enumerate(row)]
   # Print the rows using maximum column lengths
   for row in rows:
      print(' '.join(['{:>{width}}'.format(v, width = lengths[c]) for c,v in enumerate(row)]).rstrip(), file=stream)

   return lengths

def isFloatingPoint(val):
   try:
      float(val)
   except ValueError:
      # Can be parsed as a float
      return False
   try:
      int(val)
      # Can be parsed as an int
      return False
   except ValueError:
      # Can't be parsed as an int
      return True

def glob(instream, header, rows_per_glob):
   rows = []
   if len(header) > 0:
      rows.append(header)
   for row in instream:
      if len(rows) == rows_per_glob:
         yield rows
         rows = []
      rows.append(row)
   if len(rows) > 0:
      yield rows

if __name__ == "__main__":
    pp = ParameterParser('Pretty print file', columns = 0, group = False, append = False, ordered = False)
    pp.parser.add_argument('-k', '--k', type = int, default = 30, help = 'frequency in rows to recalculate column width')
    pp.parser.add_argument('-p', '--precision', type = int, default = 2, help = 'for floating point numbers, the number of digits after the decimal point to display (0 disables')
    args = pp.parseArgs()

    header = args.infile.header
    length = None
    for rows in glob(args.infile, header, args.k):
        length = printCols(rows, min_lengths = length, precision = args.precision if args.precision > 0 else None)
