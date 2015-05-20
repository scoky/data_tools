#!/usr/bin/python

import os
import sys
import argparse
import traceback
from group import Group,run_grouping

class UniqueGroup(Group):
    def __init__(self, tup):
        super(UniqueGroup, self).__init__(tup)
        self.vset = set()

    def add(self, chunks):
        val = chunks[args.column]
        self.vset.add(val)
        if args.append:
            args.outfile.write(args.jdelim.join(chunks) + args.jdelim)
        elif len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
        args.outfile.write(str(len(self.vset)) + '\n')

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute uniques counts of column(s)')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=[0])
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    args = parser.parse_args()
    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, UniqueGroup, args.group, args.delimiter, args.ordered)
