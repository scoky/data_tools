#!/usr/bin/env python

import os
import re
import sys
import argparse
import traceback
import math
from decimal import Decimal
from lib.files import findNumber,ParameterParser
from lib.group import Group,run_grouping
        
class ComputeListGroup(Group):
    def __init__(self, tup):
        super(ComputeListGroup, self).__init__(tup)
        self.lines = []

    def add(self, chunks):
        self.lines.append(chunks[args.column])

    def done(self):
        args.outfile.write(self.tup + [args.expression(self.lines)])

if __name__ == "__main__":
    pp = ParameterParser('User defined computation on a column', columns = 1, append = False, labels = [None])
    pp.parser.add_argument('-e', '--expression', help='equation to call. use l[i] to indicate row i of the list')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_list_compute']
    args = pp.getArgs(args)
    args.expression = eval('lambda l: '+ args.expression)

    run_grouping(args.infile, ComputeListGroup, args.group, args.ordered)
