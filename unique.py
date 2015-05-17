#!/usr/bin/python

import os
import sys
import argparse
import traceback
from group import Group,run_grouping

class UniqueGroup(Group):
    def __init__(self, tup):
        super(UniqueGroup, self).__init__(tup)
        self.sets = []
        for c in args.columns:
            self.sets.append(set())

    def add(self, chunks):
        vals = [chunks[i] for i in args.columns]
        for v,s in zip(vals, self.sets):
            s.add(v)

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        if len(self.tup) > 0:
            args.outfile.write(jdelim.join(self.tup) + jdelim)
        args.outfile.write(jdelim.join(map(str, map(len, self.sets))) + '\n')

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
