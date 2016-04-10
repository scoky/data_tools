#!/usr/bin/env python

import os
import sys
import argparse
from toollib.files import ParameterParser
from toollib.group import Group,run_grouping

class SetGroup(Group):
    def __init__(self, tup):
        super(SetGroup, self).__init__(tup)

    def add(self, chunks):
        if args.append:
            args.outfile.write(chunks)
        else:
            args.outfile.write(self.tup)
        self.add = self.noop
                
    def noop(self, chunks):
        pass

    def done(self):
        pass

if __name__ == "__main__":
    pp = ParameterParser('Compute the set of strings from a column in files. Maintains first appearance order.', columns = '*', ordered = False)
    args = pp.parseArgs()
    args = pp.getArgs(args)
    if not args.append and args.infile.hasHeader:
        args.outfile.header.addCols(args.columns_names)

    run_grouping(args.infile, SetGroup, args.columns, False)

