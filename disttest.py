#!/usr/bin/env python

import os
import sys
import argparse
from collections import defaultdict
from decimal import Decimal
from toollib.files import findNumber,ParameterParser
from toollib.group import Group,run_grouping
from math import sqrt

class DistGroup(Group):
    def __init__(self, tup):
        super(DistGroup, self).__init__(tup)
        self.vals = []

    def add(self, chunks):
        val = float(findNumber(chunks[args.column]))
        self.vals.append(val)

    def done(self):
        import numpy as np
        vals = np.array(self.vals)
        from scipy.stats import chisquare
        if args.pad is not None and args.pad > len(vals):
            vals = np.append(vals, [0.0] * (args.pad - len(vals)))
        args.outfile.write(self.tup + list(chisquare(vals)))

if __name__ == "__main__":
    pp = ParameterParser('Entropy of a column', columns = 1, append = False, labels = [None])
    pp.parser.add_argument('-d', '--dist', choices = ['chisquare'], default='chisquare', help='distribution test to run')
    pp.parser.add_argument('-p', '--pad', type=int, default=None, help='pad to number of potential values')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_disttest']
    args = pp.getArgs(args)

    run_grouping(args.infile, DistGroup, args.group, args.ordered)
