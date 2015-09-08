#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
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
        self.mines = []

    def add(self, chunks):
        heappush(self.mines, findNumber(chunks[args.column]))
        if len(self.mines) > args.k_max:
            heappop(self.mines)

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        if len(self.tup) > 0:
            prefix = jdelim.join(self.tup) + jdelim
        else:
            prefix = ''

        for v in sorted(self.mines):
            args.outfile.write(prefix + str(v) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute maximum of column(s)')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-k', '--k_max', type=int, default=1)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()

    if args.k_max > 1:
        run_grouping(args.infile, KMaxGroup, args.group, args.delimiter, args.ordered)
    else:
        run_grouping(args.infile, MaxGroup, args.group, args.delimiter, args.ordered)
