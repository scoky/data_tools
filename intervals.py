#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping

class IntervalGroup(Group):
    def __init__(self, tup):
        super(IntervalGroup, self).__init__(tup)
        self.last = None
        self.chunks = None

    def add(self, chunks):
        val = findNumber(chunks[args.column])
        if not args.beginning:
            args.beginning = val
        diff = val - self.last if self.last != None else val - args.beginning
        if self.last != None or args.leading:
            if args.append:
                args.outfile.write(args.jdelim.join(chunks + [str(diff)]) + '\n')
            else:
                args.outfile.write(args.jdelim.join(self.tup + [str(diff)]) + '\n')
        args.ending = self.last = val
        self.chunks = chunks

    def done(self):
        if args.ending and args.trailing:
            if args.append:
                args.outfile.write(args.jdelim.join(self.chunks + [str(args.ending - self.last)]) + '\n')
            else:
                args.outfile.write(args.jdelim.join(self.tup + [str(args.ending - self.last)]) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the difference between subsequent elements in a column')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', default=0)
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-l', '--leading', action='store_true', default=False)
    parser.add_argument('-t', '--trailing', action='store_true', default=False)
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.beginning = None
    args.ending = None
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    if args.append:
        args.outheader = args.inheader.copy()
    else:
        args.outheader = Header()
        args.outheader.addCols(args.inheader.names(args.group))
    args.outheader.addCol(args.inheader.name(args.column)+'_interval')
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.column = args.inheader.index(args.column)
    args.group = args.inheader.indexes(args.group)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, IntervalGroup, args.group, args.delimiter, args.ordered)

