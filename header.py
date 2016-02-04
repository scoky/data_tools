#!/usr/bin/python

import os
import sys
import argparse
from input_handling import FileReader,Header

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Update file header')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default=[], help='column names, use _ to leave a column unmodified')
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    args.infile = FileReader(args.infile)
    header = args.infile.Header()
    for i,c in enumerate(args.columns):
        if c != '_':
            header.setCol(c, i)
    args.outfile.write(header.value())

    for line in args.infile:
        args.outfile.write(line)

