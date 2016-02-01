#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,FileReader,Header

def compareIn(infile, outfile, columns, elements, testIn=True, delimiter=None):
    jdelim = delimiter if delimiter else ' '
    for line in infile:
        chunks = line.rstrip().split(delimiter)
        c = jdelim.join([chunks[i] for i in columns])
        if (testIn and c in elements) or (not testIn and c not in elements):
            outfile.write(line)

def main():
    elements = set()
    for item in args.element:
        elements.add(item)
    if args.listfiles:
        for listfile in args.listfiles:
            with FileReader(listfile) as f:
                for line in f:
                    elements.add(line.rstrip())

    compareIn(args.infile, args.outfile, args.columns, elements, not args.notin, args.delimiter)

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Output rows where column(s) is in list')
    parser.add_argument('element', nargs='*', help='List of elements')
    parser.add_argument('-l', '--listfiles', nargs='+', help='Files containing list elements, one per line.')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default=[0])
    parser.add_argument('-n', '--notin', action='store_true', default=False)
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    args.outheader = args.inheader.copy()
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.columns = args.inheader.indexes(args.columns)

    main()


