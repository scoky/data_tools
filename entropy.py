#!/usr/bin/env python

import os
import sys
import argparse
from collections import defaultdict
from decimal import Decimal
from toollib.files import findNumber,ParameterParser
from toollib.group import Group,run_grouping
from math import sqrt

class EntropyGroup(Group):
    def __init__(self, tup):
        super(StdGroup, self).__init__(tup)
        self.vals = []

    def add(self, chunks):
        val = findNumber(chunks[args.column])
        self.vals.append(val)

    def done(self):
        import numpy as np
        vals = np.array(self.vals) / np.sum(vals)
        from scipy.stats import entropy
        if args.pad is None or args.pad <= len(vals):
            e = entropy(vals, base = args.base)
        else:
            e = entropy(np.append(vals, [0.0] * (args.pad - len(vals)), base = args.base))
        args.outfile.write(self.tup + [e])

if __name__ == "__main__":
    pp = ParameterParser('Entropy of a column', columns = 1, append = False, labels = [None])
    pp.parser.add_argument('-p', '--pad', type=int, default=None, help='pad to number of potential values')
    pp.parser.add_argument('--base', type=float, default=None, help='pad to number of potential values')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_entropy']
    args = pp.getArgs(args)
    args.bin = args.infile.header.index(args.bin)


    run_grouping(args.infile, EntropyGroup, args.group, args.ordered)
