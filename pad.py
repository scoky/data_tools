#!/usr/bin/python

import os
import sys
import argparse
from input_handling import FileReader
from group import Group,run_grouping

class PadGroup(Group):
    def __init__(self, tup):
        super(PadGroup, self).__init__(tup)
        self.present = set()

    def add(self, chunks):
        self.present.add(args.infile.Delimiter().join(chunks[i] for i in args.columns))
        args.outfile.write(args.infile.Delimiter().join(chunks) + '\n')

    def done(self):
        for element in args.elements:
            if element not in self.present:
                args.outfile.write(args.infile.Delimiter().join(self.tup + [element] + args.pad) + '\n')
                

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Generate additional rows to pad input')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-e', '--elements', type=argparse.FileType('r'), help='File containing list elements, one per line.')
    parser.add_argument('-c', '--columns', nargs='+', default=[0])
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-p', '--pad', nargs='+', default=['0'])
    parser.add_argument('--delimiter', default=None)
    parser.add_argument('--header', action='store_true', default=False)
    args = parser.parse_args()
    args.infile = FileReader(args.infile, args.header, args.delimiter)

    # Write output header, same as input (there may not be one)
    args.outfile.write(args.infile.Header().value(args.infile.Delimiter()))
    # Get columns for use in computation
    args.columns = args.infile.Header().indexes(args.columns)

    elements = set()
    with FileReader(args.elements, args.header, args.delimiter) as f:
        for chunks in f:
            elements.add(chunks[0])
    args.elements = elements

    run_grouping(args.infile, PadGroup, args.group, ordered = False)
