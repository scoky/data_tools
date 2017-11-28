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
        self.sums = [0]*len(args.columns)
        self.count = [0]*len(args.columns)
        self.add = self.addVal if args.bins is None else self.addBin

    def addVal(self, chunks):
        for i,c in enumerate(args.columns):
            self.sums[i] += findNumber(chunks[c])
            self.count[i] += 1
        
    def addBin(self, chunks):
        for i,c in enumerate(args.columns):
            b = findNumber(chunks[args.bins[i]])
            self.sums[i] += b*findNumber(chunks[c])
            self.count[i] += b

    def done(self):
        args.outfile.write(self.tup + [s / c for s,c in zip(self.sums, self.count)])

class GeometricGroup(Group):
    def __init__(self, tup):
        super(GeometricGroup, self).__init__(tup)
        self.sums = [1]*len(args.columns)
        self.count = [0]*len(args.columns)
        self.add = self.addVal if args.bins is None else self.addBin

    def addVal(self, chunks):
        for i,c in enumerate(args.columns):
            self.sums[i] *= findNumber(chunks[c])
            self.count[i] += 1
        
    def addBin(self, chunks):
        for i,c in enumerate(args.columns):
            b = findNumber(chunks[args.bins[i]])
            self.sums[i] *= pow(findNumber(chunks[c]), b)
            self.count[i] += b

    def done(self):
        args.outfile.write(self.tup + [pow(s, 1 / c) for s,c zip(self.sums, self.count)])

if __name__ == "__main__":
    pp = ParameterParser('Compute mean of columns', columns = '*', labels = [None])
    pp.parser.add_argument('-b', '--bins', default = None, nargs='+')
    pp.parser.add_argument('-e', '--geometric', action='store_true', default=False, help='compute geometric mean')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [cn + ('_gmean' if args.geometric else '_mean') for cn in args.columns_names]
    args = pp.getArgs(args)
    if args.bin is not None:
        args.bin = args.infile.header.indexes(args.bin)

    if args.geometric:
        cls = GeometricGroup
    else:
        cls = MeanGroup
    run_grouping(args.infile, cls, args.group, args.ordered)
