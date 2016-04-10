#!/usr/bin/env python

import os
import sys
import argparse
from input_handling import ParameterParser,findNumber
from group import Group,run_grouping
from decimal import Decimal
from heapq import heappush, heappop

class MaxGroup(Group):
    def __init__(self, tup):
        super(MaxGroup, self).__init__(tup)
        self.maxes = Decimal('-Inf')
        self.rows = None

    def add(self, chunks):
        val = findNumber(chunks[args.column])
        if val > self.maxes:
            self.maxes = val
            self.rows = chunks

    def done(self):
        if args.append:
            args.outfile.write(self.rows)
        else:
            args.outfile.write(self.tup + [self.maxes])

class KMaxGroup(Group):
    def __init__(self, tup):
        super(KMaxGroup, self).__init__(tup)
        self.maxes = []

    def add(self, chunks):
        heappush(self.maxes, findNumber(chunks[args.column]))
        if len(self.maxes) > args.k:
            heappop(self.maxes)

    def done(self):
        for v in sorted(self.maxes):
            args.outfile.write(self.tup + [v])

if __name__ == "__main__":
    pp = ParameterParser('Compute maximum of column', columns = 1, labels = [None])
    pp.parser.add_argument('-k', '--k', type = int, default = 1, help = 'find the k maximum values')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_max']
    if args.append:
        args.labels = []
    args = pp.getArgs(args)

    if args.k > 1:
        run_grouping(args.infile, KMaxGroup, args.group, args.ordered)
    else:
        run_grouping(args.infile, MaxGroup, args.group, args.ordered)
