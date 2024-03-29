#!/usr/bin/env python

import os
import sys
import argparse
from collections import defaultdict
from data_tools.files import ParameterParser
from data_tools.group import Group,run_grouping

class StackGroup(Group):
    def __init__(self, tup):
        super(StackGroup, self).__init__(tup)
        self.items = defaultdict(int)
        self.count = 0

    def add(self, chunks):
        self.count += 1
        val = tuple(chunks[c] for c in args.columns)
        if val in self.items:
            val_item = self.items[val]
            distance = sum(1 for item in self.items.values() if item > val_item) # Find all items with indices larger than the last occurance of this item
        else:
            distance = -1
        self.items[val] = self.count

        if args.append:
            args.outfile.write(chunks + [distance])
        else:
            args.outfile.write(self.tup + [distance])

    def done(self):
        pass

if __name__ == "__main__":
    pp = ParameterParser('Compute the stack distance', columns = '*', labels = [None])
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = ['_'.join(args.columns_names) + '_stack_distance']
    args = pp.getArgs(args)

    run_grouping(args.infile, StackGroup, args.group, args.ordered)

