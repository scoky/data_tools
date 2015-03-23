#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper
from decimal import Decimal

class IntervalGroup(Group):
    def __init__(self, tup):
        super(IntervalGroup, self).__init__(tup)
        self.last = [None]*len(args.columns)
        self.jdelim = args.delimiter if args.delimiter != None else ' '

    def add(self, chunks):
        vals = [findNumber(chunks[i]) for i in args.columns]
        ints = [v-l if l != None else None for v,l in zip(vals,self.last)]
        args.outfile.write(self.jdelim.join(chunks+map(str, ints)) + '\n')
        self.last = vals

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the difference between subsequent elements in a column')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()

    grouper = UnsortedInputGrouper(args.infile, IntervalGroup, args.group, args.delimiter)
    grouper.group()

