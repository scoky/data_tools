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
        self.last = None
        self.jdelim = args.delimiter if args.delimiter != None else ' '

    def add(self, chunks):
        val = findNumber(chunks[args.column])
        if not args.beginning:
            args.beginning = val
        diff = val - self.last if self.last != None else val - args.beginning
        args.outfile.write(self.jdelim.join(chunks+[str(diff)]) + '\n')
        self.last = val

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the difference between subsequent elements in a column')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    args.beginning = None

    grouper = UnsortedInputGrouper(args.infile, IntervalGroup, args.group, args.delimiter)
    grouper.group()

