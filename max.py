#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping
from decimal import Decimal
from heapq import heappush, heappop

class MaxGroup(Group):
    def __init__(self, tup):
        super(MaxGroup, self).__init__(tup)
        self.maxes = Decimal('-Inf')
        self.rows = None

    def add(self, chunks):
        val = findNumber(chunks[args.column])
        if val > self.maxes:
            self.maxes = val
            self.rows = chunks

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        if args.append:
            args.outfile.write(jdelim.join(self.rows) + '\n')
        else:
            if len(self.tup) > 0:
                args.outfile.write(jdelim.join(self.tup) + jdelim)
            args.outfile.write(str(self.maxes) + '\n')

class KMaxGroup(Group):
    def __init__(self, tup):
        super(KMaxGroup, self).__init__(tup)
        self.maxes = []

    def add(self, chunks):
        heappush(self.maxes, findNumber(chunks[args.column]))
        if len(self.maxes) > args.k:
            heappop(self.maxes)

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        if len(self.tup) > 0:
            prefix = jdelim.join(self.tup) + jdelim
        else:
            prefix = ''

        for v in sorted(self.maxes):
            args.outfile.write(prefix + str(v) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute maximum of column(s)')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', default=0)
    parser.add_argument('-k', '--k', type=int, default=1)
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
    args.outheader.addCol(args.inheader.name(args.column)+'_max')
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.column = args.inheader.index(args.column)
    args.group = args.inheader.indexes(args.group)
        
    if args.k > 1:
        run_grouping(args.infile, KMaxGroup, args.group, args.delimiter, args.ordered)
    else:
        run_grouping(args.infile, MaxGroup, args.group, args.delimiter, args.ordered)
