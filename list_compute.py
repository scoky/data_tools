#!/usr/bin/python

import os
import re
import sys
import argparse
import traceback
import math
from decimal import Decimal
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping
        
class ComputeListGroup(Group):
    def __init__(self, tup):
        super(ComputeListGroup, self).__init__(tup)
        self.lines = []

    def add(self, chunks):
        self.lines.append(chunks[args.column])

    def done(self):
        if len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
        args.outfile.write(str(args.expression(self.lines)) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute maximum of column(s)')
    parser.add_argument('expression', help='equation to call. use l[i] to indicate row i of the list')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-c', '--column', default=0)
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.jdelim = args.delimiter if args.delimiter != None else ' '
    args.expression = eval('lambda l: '+ args.expression)
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    args.outheader = Header()
    args.outheader.addCols(args.inheader.names(args.group))
    args.outheader.addCol(args.inheader.name(args.column)+'_compute')
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.column = args.inheader.index(args.column)
    args.group = args.inheader.indexes(args.group)

    run_grouping(args.infile, ComputeListGroup, args.group, args.delimiter, args.ordered)
