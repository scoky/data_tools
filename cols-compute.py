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
        if not self.rows[1]:
            return
        if len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
        if args.append:
            args.outfile.write(args.jdelim.join(self.rows[1]) + args.jdelim)
        if all(self.rows):
            args.outfile.write(str(args.expression(self.rows[0], self.rows[1], self.rows[2])) + '\n')
        else:
            args.outfile.write('None\n')

    def done(self):
        self.add(None)
        
class ComputePrevGroup(Group):
    def __init__(self, tup):
        super(ComputePrevGroup, self).__init__(tup)
        self.rows = (None, None)

    def add(self, chunks):
        self.rows = (self.rows[1], chunks)
        if len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
        if args.append:
            args.outfile.write(args.jdelim.join(self.rows[1]) + args.jdelim)
        if all(self.rows):
            args.outfile.write(str(args.expression(self.rows[0], self.rows[1])) + '\n')
        else:
            args.outfile.write('None\n')

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

        if len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
        if args.append:
            args.outfile.write(args.jdelim.join(self.rows[0]) + args.jdelim)
        if all(self.rows):
            args.outfile.write(str(args.expression(self.rows[0], self.rows[1])) + '\n')
        else:
            args.outfile.write('None\n')

    def done(self):
        self.add(None)
        
class Compute1Group(Group):
    def __init__(self, tup):
        super(Compute1Group, self).__init__(tup)

    def add(self, chunks):
        if len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
        if args.append:
            args.outfile.write(args.jdelim.join(chunks) + args.jdelim)
        args.outfile.write(str(args.expression(chunks)) + '\n')

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute maximum of column(s)')
    parser.add_argument('expression', help='equation to call. use c[i] to indicate column i, p[i] to indicate column i of the previous row, and n[i] to indicate column i of the next row.')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    args = parser.parse_args()
    
    args.jdelim = args.delimiter if args.delimiter != None else ' '
    # Pattern to pull out integers which represent columns
    pattern = re.compile("([pcn]\[\d+\])")
    # Replace integers with indices into an array and convert to a lambda expression
    if 'n[' in args.expression and 'p[' in args.expression:
        args.expression = eval('lambda p,c,n: '+ pattern.sub(r'findNumber(\1)', args.expression))
        groupClass = Compute3Group
    elif 'p[' in args.expression:
        args.expression = eval('lambda p,c: '+ pattern.sub(r'findNumber(\1)', args.expression))
        groupClass = ComputePrevGroup
    elif 'n[' in args.expression:
        args.expression = eval('lambda c,n: '+ pattern.sub(r'findNumber(\1)', args.expression))
        groupClass = ComputeNextGroup
    else:
        args.expression = eval('lambda c: '+ pattern.sub(r'findNumber(\1)', args.expression))
        groupClass = Compute1Group

    grouper = UnsortedInputGrouper(args.infile, groupClass, args.group, args.delimiter)
    grouper.group()
