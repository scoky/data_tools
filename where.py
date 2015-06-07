#!/usr/bin/python

import os
import re
import sys
import argparse
import traceback
from decimal import Decimal
from input_handling import findNumber
from group import Group,UnsortedInputGrouper

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
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-f', '--findNumber', action='store_true', default=False, help='find number in column values')
    parser.add_argument('-n', '--numerical', action='store_true', default=False, help='treat columns values as numbers')
    args = parser.parse_args()
    args.numerical |= args.findNumber
    if args.numerical:
        pattern = re.compile('([pcn]\[-?\d+\])')
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
    grouper = UnsortedInputGrouper(args.infile, groupClass, args.group, args.delimiter)
    grouper.group()

