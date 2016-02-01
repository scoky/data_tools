#!/usr/bin/python

import os
import re
import sys
import argparse
import traceback
from decimal import Decimal
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping

class Compute3Group(Group):
    def __init__(self, tup):
        super(Compute3Group, self).__init__(tup)
        self.rows = (None, None, None)

    def add(self, chunks):
        self.rows = (self.rows[1], self.rows[2], chunks)
        if all(self.rows) and args.expression(self.rows[0], self.rows[1], self.rows[2]):
            args.outfile.write(args.jdelim.join(self.rows[1]) + '\n')

    def done(self):
        pass
        
class ComputePrevGroup(Group):
    def __init__(self, tup):
        super(ComputePrevGroup, self).__init__(tup)
        self.rows = (None, None)

    def add(self, chunks):
        self.rows = (self.rows[1], chunks)
        if all(self.rows) and args.expression(self.rows[0], self.rows[1]):
            args.outfile.write(args.jdelim.join(self.rows[1]) + '\n')

    def done(self):
        pass
        
class ComputeNextGroup(Group):
    def __init__(self, tup):
        super(ComputeNextGroup, self).__init__(tup)
        self.rows = (None, None)

    def add(self, chunks):
        self.rows = (self.rows[1], chunks)
        if all(self.rows) and args.expression(self.rows[0], self.rows[1]):
            args.outfile.write(args.jdelim.join(self.rows[0]) + '\n')

    def done(self):
        pass
        
class Compute1Group(Group):
    def __init__(self, tup):
        super(Compute1Group, self).__init__(tup)

    def add(self, chunks):
        if args.expression(chunks):
            args.outfile.write(args.jdelim.join(chunks) + '\n')

    def done(self):
        pass

def compare(infile, outfile, statement, delimiter):
    for line in infile:
        c = line.rstrip().split(delimiter)
        if eval(statement):
            outfile.write(line)

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Output rows where comparator is true')
    parser.add_argument('statement', default='c[0]>0', help='boolean statement to evaluate. use c[i] to indicate column i, p[i] to indicate column i of the previous row, and n[i] to indicate column i of the next row.')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-n', '--numerical', action='store_true', default=False, help='treat columns values as numbers')
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    args.outheader = args.inheader.copy()
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.group = args.inheader.indexes(args.group)

    # Replace column names with indexes from header
    pattern = re.compile("([pcn]\[([^\]\[]+)\])")
    for col in set(c for _,c in pattern.findall(args.statement)):
        ind = args.inheader.index(col)
        p = re.compile("\[%s\]" % col)
        args.statement = p.sub("[%d]" % ind, args.statement)
    if args.numerical:
        args.statement = pattern.sub(r'findNumber(\1)', args.statement)
        
    # Replace integers with indices into an array and convert to a lambda expression
    if 'n[' in args.statement and 'p[' in args.statement:
        args.expression = eval('lambda p,c,n: '+ args.statement)
        groupClass = Compute3Group
    elif 'p[' in args.statement:
        args.expression = eval('lambda p,c: '+ args.statement)
        groupClass = ComputePrevGroup
    elif 'n[' in args.statement:
        args.expression = eval('lambda c,n: '+ args.statement)
        groupClass = ComputeNextGroup
    else:
        args.expression = eval('lambda c: '+ args.statement)
        groupClass = Compute1Group

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, groupClass, args.group, args.delimiter, args.ordered)

