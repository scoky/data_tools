#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper
from collections import defaultdict

class StackGroup(Group):
    def __init__(self, tup):
        super(StackGroup, self).__init__(tup)
        self.items = defaultdict(int)

    def add(self, chunks):
        val = chunks[args.column]
        distance = self.items[val]
        self.items[val] = 0
        for key in self.items:
            self.items[key] += 1
        if args.append:
            args.outfile.write(args.jdelim.join(chunks) + args.jdelim)
        elif len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
        args.outfile.write(str(distance) + '\n')

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the stack distance of a column')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    args = parser.parse_args()
    args.jdelim = args.delimiter if args.delimiter != None else ' '

    grouper = UnsortedInputGrouper(args.infile, StackGroup, args.group, args.delimiter)
    grouper.group()
