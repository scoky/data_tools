#!/usr/bin/env python

import os
import sys
from data_tools.files import ParameterParser

def printCols(data, headers = None, stream = sys.stdout, min_lengths = None, precision = None, commas = False):
   header_widths = None
   if not (headers is None):
      header_widths = map(len, headers)
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
   float_fmt = '{:' + (',' if commas else '') + ('' if precision is None else ('.' + str(precision) + 'f')) + '}'
   int_fmt = '{:' + (',' if commas else '') + '}'
   newRows = []
   for row in rows:
      row = [int_fmt.format(int(v)) if isInt(v) else (float_fmt.format(float(v)) if isFloatingPoint(v) else v) for v in row]
      newRows.append(row)
   rows = newRows
   # Run once over the rows to find the maximum column lengths
   for row in rows:
      lengths = [max(lengths[c], len(v)) for c,v in enumerate(row)]
   # Print the rows using maximum column lengths
   for row in rows:
      print(' '.join(['{:>{width}}'.format(v, width = lengths[c]) for c,v in enumerate(row)]).rstrip(), file=stream)

   return lengths

def prettyPrintFrame(frame, output, padding = 2):
    # Get the maximum width of each column including column header and content of each row
    # Escape special characters (e.g., newline, tab) so they don't break format
    widths = [max(max(map(len,map(lambda r: str(r).encode("unicode_escape").decode("utf-8"),frame[column]))) if len(frame[column]) > 0 else 0, len(column)) for column in frame]
    # Print headers
    # padding separates the columns by padding # spaces
    print((' '*padding).join(str(r).ljust(w) for r,w in zip(frame, widths)), file=output)
    # Print row of - to separate headers from data
    print((' '*padding).join('-'*w for w in widths), file=output)
    # itertuples preserves dtype
    for row in frame.itertuples():
        # row[0] is an index, so it is excluded
        # row indices follow column order
        print((' '*padding).join(str(r).encode("unicode_escape").decode("utf-8").ljust(w) for r,w in zip(row[1:], widths)), file=output)

def isInt(val):
   try:
      int(val)
      return True
   except ValueError:
      return False

def isFloatingPoint(val):
   try:
      float(val)
      return True
   except ValueError:
      # Can't be parsed as a float
      return False

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
   pp.parser.add_argument('-p', '--precision', type = int, default = 2, help = 'for floating point numbers, the number of digits after the decimal point to display (0 disables)')
   pp.parser.add_argument('-c', '--commas', action='store_true', default=False, help = 'add commas to numbers')
   args = pp.parseArgs()

   header = args.infile.header
   length = None
   for rows in glob(args.infile, header, args.k):
      length = printCols(rows, min_lengths = length, precision = args.precision if args.precision > 0 else None, commas = args.commas)
