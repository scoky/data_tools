#!/usr/bin/env python

import os
import sys
import argparse
from decimal import Decimal
from collections import defaultdict
from lib.files import findNumber,ParameterParser
from lib.group import Group,run_grouping

class MedianGroup(Group):
    def __init__(self, tup):
        super(MedianGroup, self).__init__(tup)
        self.rows = [defaultdict(int) for c in args.columns]
        self.add = self.addBin if args.bin else self.addVal

    def addVal(self, chunks):
        for i,c in enumerate(args.columns):
            val = findNumber(chunks[c])
            self.rows[i][val] += 1
        
    def addBin(self, chunks):
        for i,c in enumerate(args.columns):
            val = findNumber(chunks[c])
            b = findNumber(chunks[args.bin])
            self.rows[i][val] += b

    def done(self):
        args.outfile.write(self.tup + [computePercentile(r) for r in self.rows])

def computePercentile(r, p=Decimal('0.5')):
    position = (sum(r.values()) + 1) * p
    ir = int(position)
    fr = Decimal(position - ir)
    count = 0
    prev = None
    for key in sorted(r.keys()):
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
    pp = ParameterParser('Compute median of a column', columns = '*', append = False, labels = [None])
    pp.parser.add_argument('-b', '--bin', default=None)
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [cn + '_median' for cn in args.columns_names]
    args = pp.getArgs(args)
    args.bin = args.infile.header.index(args.bin)

    run_grouping(args.infile, MedianGroup, args.group, args.ordered)
