#!/usr/bin/env python

import os
import sys
import argparse
from collections import defaultdict
from toollib.files import ParameterParser,findNumber
from toollib.group import Group,run_grouping

class BinGroup(Group):
    def __init__(self, tup):
        super(BinGroup, self).__init__(tup)
        if args.numerical:
            tup = [findNumber(t) for t in tup]
        self.key = tuple([args.fuzz(t) for t in tup])

    def add(self, chunks):
        args.bins[self.key] += 1

    def done(self):
        pass

class SimilarGroup(Group):
    def __init__(self, tup):
        super(SimilarGroup, self).__init__(tup)
        if args.numerical:
            tup = [findNumber(t) for t in tup]
        self.key = tuple(self.tup)
        for k in args.bins:
            if args.similar(self.key, k):
                self.key = k
                break

    def add(self, chunks):
        args.bins[self.key] += 1

    def done(self):
        pass

# Default handling of input value
def nofuzz(v):
    return v

if __name__ == "__main__":
    pp = ParameterParser('Compute bins', columns = 0, labels = [None], append = False)
    pp.parser.add_argument('-f', '--fuzz', default=None, help='lambda specifying fuzz for bins')
    pp.parser.add_argument('-s', '--similar', default=None, help='lambda specifying similarity between two arguments')
    pp.parser.add_argument('-n', '--numerical', action='store_true', default=False, help='treat the group values as numbers')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = ['_'.join(args.group_names + ['bin'])]
    args = pp.getArgs(args)
    if all((args.similar, args.fuzz)):
        raise Exception('Cannot specify both fuzz and similar')
    if not args.fuzz:
        args.fuzz = nofuzz
        cls = BinGroup
    else:
        args.fuzz = eval(args.fuzz)
        cls = BinGroup
    if args.similar:
        args.similar = eval(args.similar)
        cls = SimilarGroup

    args.bins = defaultdict(int)
    run_grouping(args.infile, cls, args.group, args.ordered)
    for k,v in args.bins.iteritems():
        args.outfile.write(list(k) + [v])
