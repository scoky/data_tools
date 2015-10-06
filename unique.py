#!/usr/bin/python

import os
import sys
import argparse
import traceback
from group import Group,run_grouping

class UniqueGroup(Group):
    def __init__(self, tup):
        super(UniqueGroup, self).__init__(tup)
        self.sets = set()
        self.jdelim = args.delimiter if args.delimiter != None else ' '

    def add(self, chunks):
        val = self.jdelim.join( (chunks[c] for c in args.columns) )
        self.sets.add(val)

    def done(self):
        if len(self.tup) > 0:
            args.outfile.write(self.jdelim.join(self.tup) + self.jdelim)
        args.outfile.write(str(len(self.sets)) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute uniques counts of column(s)')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()

    run_grouping(args.infile, UniqueGroup, args.group, args.delimiter, args.ordered)
