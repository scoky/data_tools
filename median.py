#!/usr/bin/python

import os
import sys
import argparse
from decimal import Decimal
from collections import defaultdict
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping

class MedianGroup(Group):
    def __init__(self, tup):
        super(MedianGroup, self).__init__(tup)
        self.rows = defaultdict(int)
        self.add = self.addBin if args.bin else self.addVal

    def addVal(self, chunks):
        val = findNumber(chunks[args.column])
        self.rows[val] += 1
        
    def addBin(self, chunks):
        val = findNumber(chunks[args.column])
        b = findNumber(chunks[args.bin])
        self.rows[val] += b

    def done(self):
        if len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
        args.outfile.write(str(computePercentile(self.rows)) + '\n')

def computePercentile(r, p=0.5):
    position = (sum(r.itervalues()) + 1) * p
    ir = int(position)
    fr = Decimal(position - ir)
    count = 0
    prev = None
    for key in sorted(r.iterkeys()):
        if count >= ir:
            break
        count += r[key]
        prev = key

    if prev is None:
        return key
    if fr == 0: # Whole value
        return prev
    elif count == ir: # Falls on the border between keys
        return prev * fr + key * (1 - fr)
    else: # Both median - 1 and median + 1 are same key
        return prev

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute mean of column(s)')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', default=0)
    parser.add_argument('-b', '--bin', default=None)
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    args.outheader = Header()
    args.outheader.addCols(args.inheader.names(args.group))
    args.outheader.addCol(args.inheader.name(args.column)+'_median')
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.column = args.inheader.index(args.column)
    args.group = args.inheader.indexes(args.group)
    args.bin = args.inheader.index(args.bin)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, MedianGroup, args.group, args.delimiter, args.ordered)
