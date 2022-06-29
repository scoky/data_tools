#!/usr/bin/env python

import os
import sys
import argparse
from collections import defaultdict
from decimal import Decimal
from lib.files import findNumber,ParameterParser
from lib.group import Group,run_grouping
from math import sqrt

class SkewGroup(Group):
    def __init__(self, tup):
        super(SkewGroup, self).__init__(tup)
        self.vals = []

    def add(self, chunks):
        val = float(findNumber(chunks[args.column]))

    def done(self):
        if args.pad is not None and args.pad > len(vals):
            vals = vals + [0.0] * (args.pad - len(vals))
        vals
        from scipy.stats import skew
        args.outfile.write(self.tup + list(chisquare(vals) if args.expectation is None else chisquare(vals, f_exp = expect)))

if __name__ == "__main__":
    pp = ParameterParser('Skew of the distribution', columns = 1, append = False, labels = [None])
    pp.parser.add_argument('-p', '--pad', type=int, default=None, help='pad to number of potential values')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_skew']
    args = pp.getArgs(args)
    args.expectation = args.infile.header.index(args.expectation)

    run_grouping(args.infile, SkewGroup, args.group, args.ordered)
