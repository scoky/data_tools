#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.files import findNumber,ParameterParser
from data_tools.group import Group,run_grouping

class WindowGroup(Group):
    def __init__(self, tup):
        super(WindowGroup, self).__init__(tup)
        self.cur_start = None
        self.cur_prev = None
        self.cur_count = None

    def add(self, chunks):
        val = findNumber(chunks[args.column])
        if self.cur_start is None:
            self.cur_start = val
            self.cur_prev = val
            self.cur_count = 1
        elif val - self.cur_prev > args.frequency:
            args.outfile.write(self.tup + [self.cur_start, self.cur_prev, self.cur_prev - self.cur_start, self.cur_count])
            self.cur_start = val
            self.cur_prev = val
            self.cur_count = 1
        else:
            self.cur_prev = val
            self.cur_count += 1

    def done(self):
        if not (self.cur_start is None):
            args.outfile.write(self.tup + [self.cur_start, self.cur_prev, self.cur_prev - self.cur_start, self.cur_count])

if __name__ == "__main__":
    pp = ParameterParser('Compute activity windows', columns = 1, labels = [None], append = False)
    pp.parser.add_argument('-f', '--frequency', type=float, default=0.0)
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_start', args.column_name + '_end', args.column_name + '_duration', args.column_name + '_count']
    args = pp.getArgs(args)

    run_grouping(args.infile, WindowGroup, args.group, args.ordered)

