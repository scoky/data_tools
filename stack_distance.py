#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping
from collections import defaultdict

class StackGroup(Group):
    def __init__(self, tup):
        super(StackGroup, self).__init__(tup)
        self.items = defaultdict(int)
        self.count = 0

    def add(self, chunks):
        self.count += 1
        val = args.jdelim.join( (chunks[c] for c in args.columns) )
        if val in self.items:
            val_item = self.items[val]
            distance = sum( (1 for item in self.items.itervalues() if item > val_item) ) # Find all items with indices larger than the last occurance of this item
        else:
            distance = -1
        self.items[val] = self.count

        if args.append:
            args.outfile.write(args.jdelim.join(chunks) + args.jdelim)
        elif len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim + val + args.jdelim)
        else:
            args.outfile.write(val + args.jdelim)
        args.outfile.write(str(distance) + '\n')

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the stack distance of a column')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default=[0])
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    if args.append:
        args.outheader = args.inheader.copy()
    else:
        args.outheader = Header()
        args.outheader.addCols(args.inheader.names(args.group))
        args.outheader.addCols(args.inheader.names(args.columns))
    args.outheader.addCol("_".join(args.inheader.names(args.columns)) + "_stack_distance")
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.columns = args.inheader.indexes(args.columns)
    args.group = args.inheader.indexes(args.group)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, StackGroup, args.group, args.delimiter, args.ordered)

