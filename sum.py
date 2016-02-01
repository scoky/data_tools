#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping

class SumGroup(Group):
    def __init__(self, tup):
        super(SumGroup, self).__init__(tup)
        self.sums = [0]*len(args.columns)

    def add(self, chunks):
        self.sums[:] = [s+findNumber(chunks[i]) for s,i in zip(self.sums, args.columns)]

    def done(self):
        if len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
        args.outfile.write(args.jdelim.join(map(str, self.sums)) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute sum of column(s)')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default=[0])
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    args.outheader = Header()
    args.outheader.addCols(args.inheader.names(args.group))
    for col in args.columns:
        args.outheader.addCol('%s_sum' % args.inheader.name(col))
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.columns = args.inheader.indexes(args.columns)
    args.group = args.inheader.indexes(args.group)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, SumGroup, args.group, args.delimiter, args.ordered)
