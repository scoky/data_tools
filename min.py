#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping
from decimal import Decimal
from heapq import heappush, heappop

class MinGroup(Group):
    def __init__(self, tup):
        super(MinGroup, self).__init__(tup)
        self.mines = Decimal('Inf')
        self.rows = None

    def add(self, chunks):
        val = findNumber(chunks[args.column])
        if val < self.mines:
            self.mines = val
            self.rows = chunks

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        if args.append:
            args.outfile.write(jdelim.join(self.rows) + '\n')
        else:
            if len(self.tup) > 0:
                args.outfile.write(jdelim.join(self.tup) + jdelim)
            args.outfile.write(str(self.mines) + '\n')
        
class KMinGroup(Group):
    def __init__(self, tup):
        super(KMinGroup, self).__init__(tup)
        self.mines = []

    def add(self, chunks):
        heappush(self.mines, -findNumber(chunks[args.column]))
        if len(self.mines) > args.k:
            heappop(self.mines)

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        if len(self.tup) > 0:
            prefix = jdelim.join(self.tup) + jdelim
        else:
            prefix = ''

        for v in reversed(sorted(self.mines)):
            args.outfile.write(prefix + str(-v) + '\n')
        
if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute minimum of column(s)')
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
        cls = KMinGroup
    else:
        cls = MinGroup
    run_grouping(args.infile, cls, args.group, args.delimiter, args.ordered)
