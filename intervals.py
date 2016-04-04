#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,ParameterParser
from group import Group,run_grouping

class IntervalGroup(Group):
    def __init__(self, tup):
        super(IntervalGroup, self).__init__(tup)
        self.last = None
        self.chunks = None

    def add(self, chunks):
        val = findNumber(chunks[args.column])
        if not args.beginning:
            args.beginning = val
        diff = val - self.last if self.last != None else val - args.beginning
        if self.last != None or args.leading:
            if args.append:
                args.outfile.write(chunks + [str(diff)])
            else:
                args.outfile.write(self.tup + [str(diff)])
        args.ending = self.last = val
        self.chunks = chunks

    def done(self):
        if args.ending and args.trailing:
            if args.append:
                args.outfile.write(self.chunks + [str(args.ending - self.last)])
            else:
                args.outfile.write(self.tup + [str(args.ending - self.last)])

if __name__ == "__main__":
    pp = ParameterParser('Compute the difference between subsequent elements in a column', columns = 1, labels = [None])
    pp.parser.add_argument('--leading', action='store_true', default=False)
    pp.parser.add_argument('--trailing', action='store_true', default=False)
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_interval']
    args = pp.getArgs(args)

    args.beginning = None
    args.ending = None

    run_grouping(args.infile, IntervalGroup, args.group, args.ordered)

