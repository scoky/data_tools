#!/usr/bin/python

import os
import sys
import argparse
from collections import defaultdict
from decimal import Decimal
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping
from math import sqrt

class StdGroup(Group):
    def __init__(self, tup):
        super(StdGroup, self).__init__(tup)
        self.vals = defaultdict(int)
        self.add = self.addBin if args.bin else self.addVal
        self.total = Decimal(0)
        self.count = Decimal(0)

    def addVal(self, chunks):
        val = findNumber(chunks[args.column])
        self.vals[val] += 1
        self.total += val
        self.count += 1

    def addBin(self, chunks):
        val = findNumber(chunks[args.column])
        b = findNumber(chunks[args.bin])
        self.vals[val] += b
        self.total += val*b
        self.count += b

    def done(self):
        if len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
        mean = self.total / self.count
        stddev = sqrt(sum(((val - mean)**2)*count for val,count in self.vals.iteritems()) / self.count)
        args.outfile.write(str(stddev) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute standard deviation of column(s)')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', default = 0)
    parser.add_argument('-b', '--bin', default=None)
    parser.add_argument('-g', '--group', nargs = '+', default = [])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    args.outheader = Header()
    args.outheader.addCols(args.inheader.names(args.group))
    args.outheader.addCol('%s_stddev' % args.inheader.name(args.column))
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.column = args.inheader.index(args.column)
    args.group = args.inheader.indexes(args.group)
    args.bin = args.inheader.index(args.bin)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, StdGroup, args.group, args.delimiter, args.ordered)
