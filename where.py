#!/usr/bin/env python

import os
import re
import sys
import argparse
from decimal import Decimal
from toollib.files import findNumber,ParameterParser
from toollib.group import Group,run_grouping

class Compute3Group(Group):
    def __init__(self, tup):
        super(Compute3Group, self).__init__(tup)
        self.rows = (None, None, None)

    def add(self, chunks):
        self.rows = (self.rows[1], self.rows[2], chunks)
        if all(self.rows) and (args.expression(self.rows[0], self.rows[1], self.rows[2]) != args.invert):
            args.outfile.write(self.rows[1])

    def done(self):
        pass
        
class ComputePrevGroup(Group):
    def __init__(self, tup):
        super(ComputePrevGroup, self).__init__(tup)
        self.rows = (None, None)

    def add(self, chunks):
        self.rows = (self.rows[1], chunks)
        if all(self.rows) and (args.expression(self.rows[0], self.rows[1]) != args.invert):
            args.outfile.write(self.rows[1])

    def done(self):
        pass
        
class ComputeNextGroup(Group):
    def __init__(self, tup):
        super(ComputeNextGroup, self).__init__(tup)
        self.rows = (None, None)

    def add(self, chunks):
        self.rows = (self.rows[1], chunks)
        if all(self.rows) and (args.expression(self.rows[0], self.rows[1]) != args.invert):
            args.outfile.write(self.rows[0])

    def done(self):
        pass
        
class Compute1Group(Group):
    def __init__(self, tup):
        super(Compute1Group, self).__init__(tup)

    def add(self, chunks):
        if args.expression(chunks) != args.invert:
            args.outfile.write(chunks)

    def done(self):
        pass

if __name__ == "__main__":
    pp = ParameterParser('Return only rows matching expression', columns = 0, append = False)
    pp.parser.add_argument('-n', '--numerical', action='store_true', default=False, help='treat columns values as numbers')
    pp.parser.add_argument('-v', '--invert', action='store_true', default=False)
    pp.parser.add_argument('-e', '--expression', default=None, help='boolean expression to evaluate. use c[i] to indicate column i, p[i] to indicate column i of the previous row, and n[i] to indicate column i of the next row.')
    args = pp.parseArgs()
    args.append = True
    args = pp.getArgs(args)

    # Replace column names with indexes from header
    pattern = re.compile("([pcn]\[([^\]\[]+)\])")
    for col in set(c for _,c in pattern.findall(args.expression)):
        ind = args.infile.header.index(col)
        p = re.compile("\[%s\]" % col)
        args.expression = p.sub("[%d]" % ind, args.expression)
    if args.numerical:
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

