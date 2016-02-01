#!/usr/bin/python

import os
import sys
import argparse
from decimal import Decimal
from collections import defaultdict
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping

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
        b = findNumber(chunks[args.bin])
        self.vals[val] += b

    def done(self):
        if len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
        args.outfile.write(args.jdelim.join(map(str, computePercentile(self.vals, args.percentiles))) + '\n')

def percentile(rows, pts=DEFAULT_PCT, columns=[0]):
    for c in columns:
        rows[c] = sorted(rows[c])
        indices = [int(pt*(len(rows[c])-1)) for pt in pts]
        yield [rows[c][index] for index in indices]

def computePercentile(vals, pts=DEFAULT_PCT):
    total = sum(vals.itervalues()) + 1
    positions = [total*p for p in pts]
    irs = [int(p) for p in positions]
    frs = [Decimal(p - ir) for p,ir in zip(positions,irs)]
    count = 0
    prev = None
    ind = 0
    for key in sorted(vals.iterkeys()):
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
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the percentiles')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', default=0)
    parser.add_argument('-b', '--bin', default=None)
    parser.add_argument('-p', '--percentiles', nargs='+', type=Decimal, default=DEFAULT_PCT)
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.percentiles = sorted(args.percentiles)
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    args.outheader = Header()
    args.outheader.addCols(args.inheader.names(args.group))
    for p in args.percentiles:
        args.outheader.addCol('%s_percentile_%s' % (args.inheader.name(args.column), p))
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.column = args.inheader.index(args.column)
    args.group = args.inheader.indexes(args.group)
    args.bin = args.inheader.index(args.bin)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, PercentileGroup, args.group, args.delimiter, args.ordered)

