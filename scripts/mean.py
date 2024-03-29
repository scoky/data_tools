#!/usr/bin/env python

import os
import sys
import argparse
from math import log,pow
from data_tools.files import findNumber,ParameterParser
from data_tools.group import Group,run_grouping

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
        args.outfile.write(self.tup + [pow(s, 1 / c) for s,c in zip(self.sums, self.count)])

class InvertedMeanGroup(Group):
    def __init__(self, tup):
        super(InvertedMeanGroup, self).__init__(tup)
        from collections import defaultdict
        self.vals = [[] for _ in range(len(args.columns))]
        self.add = self.addVal if args.bins is None else self.addBin

    def addVal(self, chunks):
        for i,c in enumerate(args.columns):
            v = findNumber(chunks[c])
            self.vals[i].append((v, v))

    def addBin(self, chunks):
        for i,c in enumerate(args.columns):
            self.vals[i].append((findNumber(chunks[c]), findNumber(chunks[args.bins[i]])))

    def done(self):
        import numpy as np
        m = []
        for val in self.vals:
            s = [v[0] for v in val]
            c = np.array([v[1] for v in val])
            w = (np.sum(c) / c) / np.sum(np.sum(c) / c)
            m.append(np.dot(s,w))
        args.outfile.write(self.tup + m)

if __name__ == "__main__":
    pp = ParameterParser('Compute mean of columns', columns = '*', labels = [None], append=False)
    pp.parser.add_argument('-b', '--bins', default = None, nargs='+')
    pp.parser.add_argument('-e', '--geometric', action='store_true', default=False, help='compute geometric mean')
    pp.parser.add_argument('-i', '--invert', action='store_true', default=False, help='invert the bins per value in the mean')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [cn + ('_gmean' if args.geometric else '_mean') for cn in args.columns_names]
    args = pp.getArgs(args)
    if args.bins is not None:
        args.bins = args.infile.header.indexes(args.bins)

    if args.geometric and args.invert:
        raise ValueError('Cannot specify both --geometric and --invert')
    if args.geometric:
        cls = GeometricGroup
    elif args.invert:
        cls = InvertedMeanGroup
    else:
        cls = MeanGroup
    run_grouping(args.infile, cls, args.group, args.ordered)
