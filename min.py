#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper
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
        if len(self.mines) > args.k_min:
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
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-k', '--k_min', type=int, default=1)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    args = parser.parse_args()

    if args.k_min > 1:
        grouper = UnsortedInputGrouper(args.infile, KMinGroup, args.group, args.delimiter)
    else:
        grouper = UnsortedInputGrouper(args.infile, MinGroup, args.group, args.delimiter)
    grouper.group()
