#!/usr/bin/env python

import os
import sys
from lib.files import ParameterParser

def printCols(data, headers = None, stream = sys.stdout, min_lengths = None):
   rows = []
   if headers is not None:
      rows.append(headers)
   rows.extend(data)
   # Nothing to print!
   if len(rows) == 0:
      return None

   # Set the initial lengths
   lengths = min_lengths if min_lengths is not None else [0] * len(rows[0])
   # Run once over the rows to find the maximum column lengths
   for row in rows:
      lengths = [max(lengths[c], len(v)) for c,v in enumerate(row)]
   # Print the rows using maximum column lengths
   for row in rows:
      print(' '.join(['{:>{width}}'.format(v, width = lengths[c]) for c,v in enumerate(row)]).rstrip(), file=stream)

   return lengths

def glob(instream, header, rows_per_glob):
   rows = []
   if header is not None:
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
    args = pp.parseArgs()

    header = args.infile.header if args.header else None
    length = None
    for rows in glob(args.infile, header, args.k):
        length = printCols(rows, min_lengths = length)
