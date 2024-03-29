#!/usr/bin/env python

import os
import sys
import argparse
from collections import defaultdict
from decimal import Decimal
from data_tools.files import ParameterParser,findNumber
from data_tools.group import Group,run_grouping

class ModeGroup(Group):
    def __init__(self, tup):
        super(ModeGroup, self).__init__(tup)
        self.vals = defaultdict(int)
        self.add = self.addBin if args.bin else self.addVal

    def addVal(self, chunks):
        val = findNumber(chunks[args.column])
        self.vals[val] += 1

    def addBin(self, chunks):
        val = findNumber(chunks[args.column])
        b = int(chunks[args.bin])
        self.vals[val] += b

    def done(self):
        args.outfile.write(self.tup + mode(self.vals))

def mode(dic):
    count = 0
    maximum = -1
    max_k = None
    for k,v in dic.items():
        if v > maximum:
            maximum = v
            max_k = k
        count += v
    return [max_k, maximum, count]

if __name__ == "__main__":
    pp = ParameterParser('Compute the mode of column', columns = 1, labels = [None])
    pp.parser.add_argument('-b', '--bin', default=None)
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + postfix for postfix in ('_mode', '_mode_count', '_total')]
    if args.append:
        args.labels = []
    args = pp.getArgs(args)
    args.bin = args.infile.header.index(args.bin)

    run_grouping(args.infile, ModeGroup, args.group, args.ordered)

