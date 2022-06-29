#!/usr/bin/env python

import os
import sys
import argparse
from lib.files import ParameterParser,findNumber
from lib.group import Group,run_grouping
from decimal import Decimal
from heapq import heappush, heappop

class MinGroup(Group):
    def __init__(self, tup):
        super(MinGroup, self).__init__(tup)
        self.mines = Decimal('Inf')
        self.rows = None

    def add(self, chunks):
        val = findNumber(chunks[args.column])
        if val < self.mines:
            self.mines = val
            self.rows = chunks

    def done(self):
        if args.append:
            args.outfile.write(self.rows)
        else:
            args.outfile.write(self.tup + [self.mines])
        
class KMinGroup(Group):
    def __init__(self, tup):
        super(KMinGroup, self).__init__(tup)
        self.mines = []

    def add(self, chunks):
        heappush(self.mines, -findNumber(chunks[args.column]))
        if len(self.mines) > args.k:
            heappop(self.mines)

    def done(self):
        for v in reversed(sorted(self.mines)):
            args.outfile.write(self.tup + [-v])
        
if __name__ == "__main__":
    pp = ParameterParser('Compute minimum of column', columns = 1, labels = [None])
    pp.parser.add_argument('-k', '--k', type = int, default = 1, help = 'find the k minimum values')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_min']
    if args.append:
        args.labels = []
    args = pp.getArgs(args)

    if args.k > 1:
        cls = KMinGroup
    else:
        cls = MinGroup
    run_grouping(args.infile, cls, args.group, args.ordered)
