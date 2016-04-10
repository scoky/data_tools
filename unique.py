#!/usr/bin/env python

import os
import sys
import argparse
from toollib.files import ParameterParser
from toollib.group import Group,run_grouping

class UniqueGroup(Group):
    def __init__(self, tup):
        super(UniqueGroup, self).__init__(tup)
        self.sets = set()

    def add(self, chunks):
        val = tuple(chunks[c] for c in args.columns)
        self.sets.add(val)

    def done(self):
        args.outfile.write(self.tup + [len(self.sets)])

if __name__ == "__main__":
    pp = ParameterParser('Compute uniques counts of column(s)', columns = '*', append = False, labels = [None])
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = ['_'.join(args.columns_names) + '_uniques']
    args = pp.getArgs(args)

    run_grouping(args.infile, UniqueGroup, args.group, args.ordered)
