#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,FileReader,Header

def columns(infile, outfile, cols, delimiter):
    jdelim = delimiter if delimiter != None else ' '
    for line in infile:
        try:
            chunks = line.rstrip().split(delimiter)
        except Exception as e:
            logging.error('Error on input: %s\n%s', line, e)
            continue
        outfile.write(jdelim.join([chunks[i] for i in cols])+'\n')

def main():
    columns(args.infile, args.outfile, args.columns, args.delimiter)

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Select columns from a file.')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default='0', help='can specify column indices, or ranges (e.g., 0:4)')
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    args.outheader = Header()

    cols = args.columns
    args.columns = []
    for c in cols:
        vals = c.split(':', 1)
        args.outheader.addCols(args.inheader.names(vals))
        indexes = args.inheader.indexes(vals)
        if len(vals) == 1:
            args.columns.append(args.inheader.index(indexes[0]))
        elif len(vals) == 2:
            args.columns.extend(range(indexes[0], indexes[1] + 1))
        else:
            raise Exception('invalid column parameter')

    # Write output header
    args.outfile.write(args.outheader.value())

    main()

