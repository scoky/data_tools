#!/usr/bin/env python

import os
import sys
import argparse
from decimal import Decimal
from collections import defaultdict
from data_tools.files import findNumber,ParameterParser
from data_tools.group import Group,run_grouping

DEFAULT_PCT = list(map(Decimal, ['0', '0.01', '0.25', '0.5', '0.75', '0.99', '1']))

class PercentileGroup(Group):
    def __init__(self, tup):
        super(PercentileGroup, self).__init__(tup)
        self.vals = [defaultdict(int) for c in args.columns]
        self.add = self.addBin if args.bin else self.addVal

    def addVal(self, chunks):
        for i,c in enumerate(args.columns):
            val = findNumber(chunks[c])
            self.vals[i][val] += 1

    def addBin(self, chunks):
        for i,c in enumerate(args.columns):
            val = findNumber(chunks[c])
            b = findNumber(chunks[args.bin])
            self.vals[i][val] += b

    def done(self):
        output = self.tup
        for v in self.vals:
            output += list(computePercentile(v, args.percentiles))
        args.outfile.write(output)

def percentile(rows, pts=DEFAULT_PCT, columns=[0]):
    for c in columns:
        rows[c] = sorted(rows[c])
        indices = [int(pt*(len(rows[c])-1)) for pt in pts]
        yield [rows[c][index] for index in indices]

def computePercentile(vals, pts=DEFAULT_PCT):
    total = sum(vals.values()) + 1
    positions = [total*p for p in pts]
    irs = [int(p) for p in positions]
    frs = [Decimal(p - ir) for p,ir in zip(positions,irs)]
    count = 0
    prev = None
    ind = 0
    for key in sorted(vals.keys()):
        while count >= irs[ind]:
            if prev is None:
                yield key
            elif frs[ind] == 0 or count != irs[ind]: # Whole value
                yield prev
            else: # Falls on the border between keys
                yield prev * frs[ind] + key * (1 - frs[ind])

            ind += 1
            if ind >= len(pts):
                return
        count += vals[key]
        prev = key
    # Report remaining percentiles
    while ind < len(pts):
        yield key
        ind += 1

if __name__ == "__main__":
    pp = ParameterParser('Compute percentiles from a column', columns = '*', append = False, labels = [None])
    pp.parser.add_argument('-b', '--bin', default=None)
    pp.parser.add_argument('-p', '--percentiles', nargs='+', type=Decimal, default=DEFAULT_PCT)
    args = pp.parseArgs()
    args.percentiles = sorted(args.percentiles)
    if not any(args.labels):
        args.labels = ['{0}_ptile{1}'.format(cn, p) for cn in args.columns_names for p in args.percentiles]
    args = pp.getArgs(args)
    args.bin = args.infile.header.index(args.bin)

    run_grouping(args.infile, PercentileGroup, args.group, args.ordered)
