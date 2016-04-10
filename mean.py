#!/usr/bin/env python

import os
import sys
import argparse
from math import log,pow
from toollib.files import findNumber,ParameterParser
from toollib.group import Group,run_grouping

class MeanGroup(Group):
    def __init__(self, tup):
        super(MeanGroup, self).__init__(tup)
        self.sums = 0
        self.count = 0
        self.add = self.addVal if args.bin is None else self.addBin

    def addVal(self, chunks):
        self.sums += findNumber(chunks[args.column])
        self.count += 1
        
    def addBin(self, chunks):
        b = findNumber(chunks[args.bin])
        self.sums += b*findNumber(chunks[args.column])
        self.count += b

    def done(self):
        args.outfile.write(self.tup + [self.sums / self.count])

class GeometricGroup(Group):
    def __init__(self, tup):
        super(GeometricGroup, self).__init__(tup)
        self.sums = 1
        self.count = 0
        self.add = self.addVal if args.bin is None else self.addBin

    def addVal(self, chunks):
        self.sums *= findNumber(chunks[args.column])
        self.count += 1
        
    def addBin(self, chunks):
        b = findNumber(chunks[args.bin])
        self.sums *= pow(findNumber(chunks[args.column]), b)
        self.count += b

    def done(self):
        args.outfile.write(self.tup + [pow(self.sums, 1 / self.count)])

if __name__ == "__main__":
    pp = ParameterParser('Compute mean of column', columns = 1, labels = [None])
    pp.parser.add_argument('-b', '--bin', default=None)
    pp.parser.add_argument('-e', '--geometric', action='store_true', default=False, help='compute geometric mean')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + ('_gmean' if args.geometric else '_mean')]
    args = pp.getArgs(args)
    args.bin = args.infile.header.index(args.bin)

    if args.geometric:
        cls = GeometricGroup
    else:
        cls = MeanGroup
    run_grouping(args.infile, cls, args.group, args.ordered)
