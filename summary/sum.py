#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,ParameterParser
from group import Group,run_grouping

class SumGroup(Group):
    def __init__(self, tup):
        super(SumGroup, self).__init__(tup)
        self.sums = 0

    def add(self, chunks):
        self.sums += findNumber(chunks[args.column])

    def done(self):
        args.outfile.write(self.tup + [self.sums])

if __name__ == "__main__":
    pp = ParameterParser('Sum of column', columns = 1, append = False, labels = [None])
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_sum']
    args = pp.getArgs(args)

    run_grouping(args.infile, SumGroup, args.group, args.ordered)
