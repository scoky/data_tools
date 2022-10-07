#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.files import ParameterParser,findNumber
from data_tools.group import Group,run_grouping
from decimal import Decimal

class NormalizeGroup(Group):
    def __init__(self, tup):
        super(NormalizeGroup, self).__init__(tup)
        self.value = 0
        args.collect.append(self)

    def add(self, chunks):
        self.value += findNumber(chunks[args.column])

    def done(self):
        pass

if __name__ == "__main__":
    pp = ParameterParser('Normalize values in column', columns = 1, append = False, labels = [None])
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_norm']
    args = pp.getArgs(args)
    args.collect = []

    run_grouping(args.infile, NormalizeGroup, args.group, args.ordered)

    mvalue = max(g.value for g in args.collect)
    for g in args.collect:
        args.outfile.write(g.tup + [g.value / mvalue])
