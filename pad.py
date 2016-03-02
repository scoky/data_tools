#!/usr/bin/python

import os
import sys
import argparse
from input_handling import FileReader,Header
from group import Group,run_grouping

class PadGroup(Group):
    def __init__(self, tup):
        super(PadGroup, self).__init__(tup)
        self.present = set()

    def add(self, chunks):
        self.present.add(chunks[args.column])
        args.outfile.write(args.jdelim.join(chunks) + '\n')

    def done(self):
        for element in args.elements:
            if element not in self.present:
                args.outfile.write((args.pad + '\n') % (args.jdelim.join(self.tup), element))
                

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Generate additional rows to pad input')
    parser.add_argument('infile', nargs='?', type=FileReader, default=FileReader(sys.stdin))
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-e', '--elements', help='File containing list elements, one per line.')
    parser.add_argument('-c', '--columns', nargs='+', default=[0])
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-p', '--pad', default='0')
    args = parser.parse_args()

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    args.outheader = Header()
    args.outheader.addCols(args.inheader.names(args.group))
    args.outheader.addCol(args.inheader.names(args.columns))
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.column = args.inheader.index(args.column)
    args.group = args.inheader.indexes(args.group)
        
    if args.k > 1:
        run_grouping(args.infile, KMaxGroup, args.group, args.delimiter, args.ordered)

    
    args.jdelim = args.delimiter if args.delimiter else ' '
    args.elements = set()
    with open(args.listfile, 'r') as f:
        for line in f:
            args.elements.add(line.rstrip())

    grouper = UnsortedInputGrouper(args.infile, PadGroup, args.group, args.delimiter)
    grouper.group()
