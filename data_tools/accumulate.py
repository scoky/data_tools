#!/usr/bin/env python

import os
import sys
import argparse
from lib.files import findNumber,ParameterParser
from lib.group import Group,run_grouping

class AccumulateGroup(Group):
    def __init__(self, tup):
        super(AccumulateGroup, self).__init__(tup)
        self.total = 0

    def add(self, chunks):
        self.total += findNumber(chunks[args.column])
        if args.append:
            args.outfile.write(chunks + [self.total])
        else:
            args.outfile.write(self.tup + [self.total])

    def done(self):
        pass

if __name__ == "__main__":
    pp = ParameterParser('Accumulate the values of a column(s)', columns = 1, labels = [None])
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_accumulate']
    args = pp.getArgs(args)

    run_grouping(args.infile, AccumulateGroup, args.group, args.ordered)

