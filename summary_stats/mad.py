#!/usr/bin/env python

import os
import sys
import argparse
from collections import defaultdict
from decimal import Decimal
from input_handling import findNumber,ParameterParser
from group import Group,run_grouping
from math import sqrt
from median import computePercentile

class MadGroup(Group):
    def __init__(self, tup):
        super(MadGroup, self).__init__(tup)
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
        median = computePercentile(self.vals)
        mad = computePercentile({ abs(val - median) : count for val,count in self.vals.iteritems() })
        args.outfile.write(self.tup + [mad])

class PreMadGroup(Group):
    def __init__(self, tup):
        super(PreMadGroup, self).__init__(tup)
        self.add = self.addBin if args.bin else self.addVal
        self.vals = defaultdict(int)

    def addVal(self, chunks):
        val = abs(findNumber(chunks[args.column]) - args.median)
        self.vals[val] += 1

    def addBin(self, chunks):
        val = abs(findNumber(chunks[args.column]) - args.median)
        b = findNumber(chunks[args.bin])
        self.vals[val] += b

    def done(self):
        mad = computePercentile(self.vals)
        args.outfile.write(self.tup + [mad])

if __name__ == "__main__":
    pp = ParameterParser('Median absolute difference of a column', columns = 1, append = False, labels = [None])
    pp.parser.add_argument('-b', '--bin', default=None)
    pp.parser.add_argument('-m', '--median', default=None)
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_mad']
    args = pp.getArgs(args)
    args.bin = args.infile.header.index(args.bin)

    if args.median:
        args.median = Decimal(args.median)
        run_grouping(args.infile, PreMadGroup, args.group, args.ordered)
    else:
        run_grouping(args.infile, MadGroup, args.group, args.ordered)
