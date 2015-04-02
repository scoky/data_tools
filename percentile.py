#!/usr/bin/python

import os
import sys
import argparse
import traceback
from collections import defaultdict
from decimal import Decimal
from input_handling import findNumber
from group import Group,UnsortedInputGrouper

DEFAULT_PCT = map(Decimal, ['0', '0.01', '0.25', '0.5', '0.75', '0.99', '1'])

class PercentileGroup(Group):
    def __init__(self, tup):
        super(PercentileGroup, self).__init__(tup)
        self.vals = defaultdict(int)
        self.add = self.addBin if args.bin else self.addVal

    def addVal(self, chunks):
        val = findNumber(chunks[args.column])
        self.vals[val] += 1

    def addBin(self, chunks):
        val = findNumber(chunks[args.column])
        b = int(chunks[args.bin])
        self.vals[val] += b

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        if len(self.tup) > 0:
            args.outfile.write(jdelim.join(self.tup) + jdelim)
        args.outfile.write(jdelim.join(map(str, percentileDict(self.vals, args.percentiles))) + '\n')

def percentile(rows, pts=DEFAULT_PCT, columns=[0]):
    for c in columns:
        rows[c] = sorted(rows[c])
        indices = [int(pt*(len(rows[c])-1)) for pt in pts]
        yield [rows[c][index] for index in indices]

def percentileDict(dic, pts=DEFAULT_PCT):
    count = sum(dic.itervalues())
    indices = [int(pt*(count-1)) for pt in pts]
    count = 0
    for k in sorted(dic):
        count += dic[k]
        while len(indices) > 0 and indices[0] < count:
            yield k
            indices.remove(indices[0])

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the percentiles of a two column format')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-b', '--bin', type=int, default=None)
    parser.add_argument('-p', '--percentiles', nargs='+', type=Decimal, default=DEFAULT_PCT)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()

    grouper = UnsortedInputGrouper(args.infile, PercentileGroup, args.group, args.delimiter)
    grouper.group()

