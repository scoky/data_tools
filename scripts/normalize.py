#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.files import ParameterParser,findNumber
from data_tools.group import Group,run_grouping
from decimal import Decimal,InvalidOperation

class NormalizeGroup(Group):
    def __init__(self, tup):
        super(NormalizeGroup, self).__init__(tup)
        self.values = []

    def add(self, chunks):
        self.values.append(chunks)

    # def done(self):
    #     maxv = max(findNumber(chunks[args.column]) for chunks in self.values)
    #     minv = min(findNumber(chunks[args.column]) for chunks in self.values)
    #     for chunks in self.values:
    #         value = findNumber(chunks[args.column])
    #         value = ((value - minv) / (maxv - minv)) * (args.range[1] - args.range[0]) + args.range[0]
    #         if args.append:
    #             args.outfile.write(chunks + [value])
    #         else:
    #             args.outfile.write(self.tup + [value])

    def done(self):
        import numpy as np
        vals = np.array([findNumber(chunks[args.column]) for chunks in self.values])
        try:
            vals = (vals - vals.mean()) / vals.std()
        except InvalidOperation:
            # std is 0, which means vals are constant
            vals = (vals - vals.mean())
        if not args.range is None:
            vals = ((vals - vals.min()) / (vals.max() - vals.min())) * (args.range[1] - args.range[0]) + args.range[0]
        if args.append:
            for value,chunks in zip(vals, self.values):
                args.outfile.write(chunks + [value])
        else:
            for value in vals:
                args.outfile.write(self.tup + [value])

if __name__ == "__main__":
    pp = ParameterParser('Normalize values in column', columns = 1, append = True, labels = [None])
    pp.parser.add_argument('-r', '--range', nargs=2, type=int, default=None, help='normalization range')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_norm']
    args = pp.getArgs(args)

    run_grouping(args.infile, NormalizeGroup, args.group, args.ordered)
