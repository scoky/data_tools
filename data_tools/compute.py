#!/usr/bin/env python

import os
import re
import sys
import argparse
from decimal import Decimal
from lib.files import findNumber,ParameterParser
from lib.group import Group,run_grouping
import math

class Compute3Group(Group):
    def __init__(self, tup):
        super(Compute3Group, self).__init__(tup)
        self.rows = (None, None, None)

    def add(self, chunks):
        self.rows = (self.rows[1], self.rows[2], chunks)
        if not self.rows[1]:
            return
            
        val = args.expression(self.rows[0], self.rows[1], self.rows[2]) if all(self.rows) else None
        if args.append:
            args.outfile.write(self.rows[1] + [val])
        else:
            args.outfile.write(self.tup + [val])

    def done(self):
        self.add(None)
        
class ComputePrevGroup(Group):
    def __init__(self, tup):
        super(ComputePrevGroup, self).__init__(tup)
        self.rows = (None, None)

    def add(self, chunks):
        self.rows = (self.rows[1], chunks)

        val = args.expression(self.rows[0], self.rows[1]) if all(self.rows) else None
        if args.append:
            args.outfile.write(self.rows[1] + [val])
        else:
            args.outfile.write(self.tup + [val])

    def done(self):
        pass
        
class ComputeNextGroup(Group):
    def __init__(self, tup):
        super(ComputeNextGroup, self).__init__(tup)
        self.rows = (None, None)

    def add(self, chunks):
        self.rows = (self.rows[1], chunks)
        if not self.rows[0]:
            return

        val = args.expression(self.rows[0], self.rows[1]) if all(self.rows) else None
        if args.append:
            args.outfile.write(self.rows[0] + [val])
        else:
            args.outfile.write(self.tup + [val])

    def done(self):
        self.add(None)
        
class Compute1Group(Group):
    def __init__(self, tup):
        super(Compute1Group, self).__init__(tup)

    def add(self, chunks):
        if args.append:
            args.outfile.write(chunks + [args.expression(chunks)])
        else:
            args.outfile.write(self.tup + [args.expression(chunks)])

    def done(self):
        pass

if __name__ == "__main__":
    pp = ParameterParser('User defined computation on rows', columns = 0, labels = [None])
    pp.parser.add_argument('-n', '--numerical', action='store_true', default=False, help='treat columns values as numbers')
    pp.parser.add_argument('-e', '--expression', help='equation to call. use c[i] to indicate column i, p[i] to indicate column i of the previous row, and n[i] to indicate column i of the next row.')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = ['compute']
    args = pp.getArgs(args)

    # Replace column names with indexes from header
    pattern = re.compile("([pcn]\[([^\]\[]+)\])")
    for col in set(c for _,c in pattern.findall(args.expression)):
        ind = args.infile.header.index(col)
        p = re.compile("\[%s\]" % col)
        args.expression = p.sub("[%d]" % ind, args.expression)
    # Interpret as numbers
    if args.numerical:
        # Pattern to pull out integers which represent columns
        args.expression = pattern.sub(r'findNumber(\1)', args.expression)

    # Replace integers with indices into an array and convert to a lambda expression
    if 'n[' in args.expression and 'p[' in args.expression:
        args.expression = eval('lambda p,c,n: '+ args.expression)
        groupClass = Compute3Group
    elif 'p[' in args.expression:
        args.expression = eval('lambda p,c: '+ args.expression)
        groupClass = ComputePrevGroup
    elif 'n[' in args.expression:
        args.expression = eval('lambda c,n: '+ args.expression)
        groupClass = ComputeNextGroup
    else:
        args.expression = eval('lambda c: '+ args.expression)
        groupClass = Compute1Group

    run_grouping(args.infile, groupClass, args.group, args.ordered)
