#!/usr/bin/python

import os
import re
import sys
import argparse
from decimal import Decimal
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping

class Compute3Group(Group):
    def __init__(self, tup):
        super(Compute3Group, self).__init__(tup)
        self.rows = (None, None, None)

    def add(self, chunks):
        self.rows = (self.rows[1], self.rows[2], chunks)
        if not self.rows[1]:
            return
        if args.append:
            args.outfile.write(args.jdelim.join(self.rows[1]) + args.jdelim)
        elif len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)

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

        if args.append:
            args.outfile.write(args.jdelim.join(self.rows[1]) + args.jdelim)
        elif len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)

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

        if args.append:
            args.outfile.write(args.jdelim.join(self.rows[0]) + args.jdelim)
        elif len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)

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
        if args.append:
            args.outfile.write(args.jdelim.join(chunks) + args.jdelim)
        elif len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
        args.outfile.write(str(args.expression(chunks)) + '\n')

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute maximum of column(s)')
    parser.add_argument('expression', help='equation to call. use c[i] to indicate column i, p[i] to indicate column i of the previous row, and n[i] to indicate column i of the next row.')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-n', '--numerical', action='store_true', default=False, help='treat columns values as numbers')
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    if args.append:
        args.outheader = args.inheader.copy()
    else:
        args.outheader = Header()
        args.outheader.addCols(args.inheader.names(args.group))
    args.outheader.addCol('compute')
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.group = args.inheader.indexes(args.group)

    args.jdelim = args.delimiter if args.delimiter != None else ' '

    # Replace column names with indexes from header
    pattern = re.compile("([pcn]\[([^\]\[]+)\])")
    for col in set(c for _,c in pattern.findall(args.expression)):
        ind = args.inheader.index(col)
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

    run_grouping(args.infile, groupClass, args.group, args.delimiter, args.ordered)
