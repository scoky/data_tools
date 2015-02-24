#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper
from decimal import Decimal

class MaxGroup(Group):
    def __init__(self, tup):
        super(MaxGroup, self).__init__(tup)
        self.maxes = [Decimal('-Inf')]*len(args.columns)

    def add(self, chunks):
        vals = [findNumber(chunks[i]) for i in args.columns]
        self.maxes = map(max, self.maxes, vals)

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        if len(self.tup) > 0:
            args.outfile.write(jdelim.join(self.tup) + jdelim)
        args.outfile.write(jdelim.join(map(str, self.maxes)) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute maximum of column(s)')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()

    grouper = UnsortedInputGrouper(args.infile, MaxGroup, args.group, args.delimiter)
    grouper.group()
