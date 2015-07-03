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
        self.chunks = None

    def add(self, chunks):
        val = findNumber(chunks[args.column])
        if not args.beginning:
            args.beginning = val
        diff = val - self.last if self.last != None else val - args.beginning
        if self.last != None or args.leading:
            args.outfile.write(self.jdelim.join(chunks+[str(diff)]) + '\n')
        args.ending = self.last = val
        self.chunks = chunks

    def done(self):
        if args.ending and args.trailing:
            args.outfile.write(self.jdelim.join(self.chunks+[str(args.ending - self.last)]) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the difference between subsequent elements in a column')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-l', '--leading', action='store_true', default=False)
    parser.add_argument('-t', '--trailing', action='store_true', default=False)
    args = parser.parse_args()
    args.beginning = None
    args.ending = None

    grouper = UnsortedInputGrouper(args.infile, IntervalGroup, args.group, args.delimiter)
    grouper.group()

