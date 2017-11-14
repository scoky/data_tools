#!/usr/bin/env python

import os
import sys
import argparse
from toollib.files import findNumber,ParameterParser
from toollib.group import Group,run_grouping

class SumGroup(Group):
    def __init__(self, tup):
        super(SumGroup, self).__init__(tup)
        self.sums = [0]*len(args.columns)

    def add(self, chunks):
        for i,c in args.columns:
            self.sums[i] += findNumber(chunks[c])

    def done(self):
        args.outfile.write(self.tup + self.sums)

if __name__ == "__main__":
    pp = ParameterParser('Sum of column', columns = '*', append = False, labels = [None])
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [cn + '_sum' for cn in args.columns_names]
    args = pp.getArgs(args)

    run_grouping(args.infile, SumGroup, args.group, args.ordered)
