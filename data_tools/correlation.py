#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.lib.files import findNumber,ParameterParser
from data_tools.lib.group import Group,run_grouping
from numpy import corrcoef

class CorrelationGroup(Group):
    def __init__(self, tup):
        super(CorrelationGroup, self).__init__(tup)
        self.vals = []

    def add(self, chunks):
        self.vals.append([float(findNumber(chunks[i])) for i in args.columns])

    def done(self):
        if len(self.vals) > 1 and len(self.vals[0]) > 1:
            v = corrcoef(self.vals, rowvar=0)
            for i,row in enumerate(v):
                for j in range(i):
                    args.outfile.write(self.tup + [args.columns_names[i], args.columns_names[j], row[j]])

if __name__ == "__main__":
    pp = ParameterParser('Compute correlation of 2 or more columns', columns = '*', append = False)
    args = pp.parseArgs()
    args.labels = ['col1', 'col2', 'correlation']
    args = pp.getArgs(args)

    run_grouping(args.infile, CorrelationGroup, args.group, args.ordered)

