#!/usr/bin/env python

import os
import sys
import argparse
from collections import defaultdict
from decimal import Decimal
from lib.files import findNumber,ParameterParser
from lib.group import Group,run_grouping
from math import sqrt

class StdGroup(Group):
    def __init__(self, tup):
        super(StdGroup, self).__init__(tup)
        self.vals = defaultdict(int)
        self.add = self.addBin if args.bin else self.addVal
        self.total = Decimal(0)
        self.count = Decimal(0)

    def addVal(self, chunks):
        val = findNumber(chunks[args.column])
        self.vals[val] += 1
        self.total += val
        self.count += 1

    def addBin(self, chunks):
        val = findNumber(chunks[args.column])
        b = findNumber(chunks[args.bin])
        self.vals[val] += b
        self.total += val*b
        self.count += b

    def done(self):
        mean = self.total / self.count
        stddev = sqrt(sum(((val - mean)**2)*count for val,count in self.vals.items()) / self.count)
        args.outfile.write(self.tup + [stddev])

class PreStdGroup(Group):
    def __init__(self, tup):
        super(PreStdGroup, self).__init__(tup)
        self.add = self.addBin if args.bin else self.addVal
        self.total = Decimal(0)
        self.count = 0

    def addVal(self, chunks):
        val = findNumber(chunks[args.column])
        self.total += (val - args.mean)**2
        self.count += 1

    def addBin(self, chunks):
        val = findNumber(chunks[args.column])
        b = findNumber(chunks[args.bin])
        self.total += ((val - args.mean)**2)*b
        self.count += b

    def done(self):
        stddev = sqrt(self.total / self.count)
        args.outfile.write(self.tup + [stddev])

if __name__ == "__main__":
    pp = ParameterParser('Standard deviation of a column', columns = 1, append = False, labels = [None])
    pp.parser.add_argument('-b', '--bin', default=None)
    pp.parser.add_argument('-m', '--mean', default=None, help='precomputed mean')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_stddev']
    args = pp.getArgs(args)
    args.bin = args.infile.header.index(args.bin)

    if args.mean:
        args.mean = Decimal(args.mean)
        run_grouping(args.infile, PreStdGroup, args.group, args.ordered)
    else:
        run_grouping(args.infile, StdGroup, args.group, args.ordered)
