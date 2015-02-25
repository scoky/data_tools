#!/usr/bin/python

import os
import sys
import argparse
import traceback
from decimal import Decimal
from input_handling import findNumber
from group import Group,UnsortedInputGrouper

DEFAULT_PCT = map(Decimal, ['0', '0.01', '0.25', '0.5', '0.75', '0.99', '1'])

class PercentileGroup(Group):
    def __init__(self, tup):
        super(PercentileGroup, self).__init__(tup)
        self.rows = [[] for i in args.columns]

    def add(self, chunks):
        vals = [findNumber(chunks[i]) for i in args.columns]
        for v,r in zip(vals, self.rows):
            r.append(v)

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        for c,p in zip(args.columns, percentile(self.rows, args.percentiles, range(len(self.rows)))):
            if len(self.tup) > 0:
                args.outfile.write(jdelim.join(self.tup) + jdelim)
            args.outfile.write(str(c) + jdelim + jdelim.join(map(str, p)) + '\n')

def percentile(rows, pts=DEFAULT_PCT, columns=[0]):
    for c in columns:
        rows[c] = sorted(rows[c])
        indices = [int(pt*(len(rows[c])-1)) for pt in pts]
        yield [rows[c][index] for index in indices]

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the percentiles of a two column format')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-p', '--percentiles', nargs='+', type=Decimal, default=DEFAULT_PCT)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()

    grouper = UnsortedInputGrouper(args.infile, PercentileGroup, args.group, args.delimiter)
    grouper.group()

