#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper
from numpy import power,sqrt,median

class StdGroup(Group):
    def __init__(self, tup):
        super(StdGroup, self).__init__(tup)
        self.rows = [[] for i in args.columns]

    def add(self, chunks):
        vals = [findNumber(chunks[i]) for i in args.columns]
        for v,r in zip(vals, self.rows):
            r.append(v)

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        if len(self.tup) > 0:
            prefix = jdelim.join(self.tup) + jdelim
        else:
            prefix = ''
        for r in self.rows:
            m = median(r)
            s = sqrt(sum( (power(v - m, 2) for v in r) ) / len(r))
            args.outfile.write(prefix + str(s) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute deviation from median of column(s)')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()

    grouper = UnsortedInputGrouper(args.infile, StdGroup, args.group, args.delimiter)
    grouper.group()
