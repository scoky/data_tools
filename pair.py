#!/usr/bin/python

import os
import sys
import argparse
import traceback
from group import Group,run_grouping

class PairGroup(Group):
    def __init__(self, tup):
        super(PairGroup, self).__init__(tup)
        self.items = set()

    def add(self, chunks):
        val = chunks[args.column]
        if val not in self.items:
            for item in self.items:
                if len(self.tup) > 0:
                    args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
                if val <= item:
                    args.outfile.write(val + args.jdelim + item + '\n')
                else:
                    args.outfile.write(item + args.jdelim + val + '\n')
            self.items.add(val)

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute all pairs of inputs')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, PairGroup, args.group, args.delimiter, args.ordered)
