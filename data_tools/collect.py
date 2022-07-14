#!/usr/bin/env python

import os
import sys
import argparse
from math import log,pow
from lib.files import findNumber,ParameterParser
from lib.group import Group,run_grouping

class CollectGroup(Group):
    def __init__(self, tup):
        super(CollectGroup, self).__init__(tup)
        self.collects = [[] for _ in range(len(args.columns))]

    def add(self, chunks):
        for i,c in enumerate(args.columns):
            self.collects[i].append(chunks[c])

    def done(self):
        args.outfile.write(self.tup + [args.join.join(c) for c in self.collects])

class ReverseCollectGroup(Group):
    def __init__(self, tup):
        super(ReverseCollectGroup, self).__init__(tup)

    def add(self, chunks):
        for c in args.columns:
            for cc in chunks[c].split(args.join):
                if args.append:
                    args.outfile.write(chunks + [cc])
                else:
                    args.outfile.write([cc])

if __name__ == "__main__":
    pp = ParameterParser('Compute mean of columns', columns = '*', labels = [None])
    pp.parser.add_argument('-j', '--join', default=' ', help='character to use to join values together')
    pp.parser.add_argument('-r', '--reverse', action='store_true', help='reverse the collection')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [cn + '_collect' for cn in args.columns_names]
    args = pp.getArgs(args)
    if args.reverse:
        run_grouping(args.infile, ReverseCollectGroup, args.group, args.ordered)
    else:
        run_grouping(args.infile, CollectGroup, args.group, args.ordered)
