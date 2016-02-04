#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping
from numpy import corrcoef

class CorrelationGroup(Group):
    def __init__(self, tup):
        super(CorrelationGroup, self).__init__(tup)
        self.vals = []

    def add(self, chunks):
        self.vals.append([float(findNumber(chunks[i])) for i in args.columns])

    def done(self):
        if len(self.tup) > 0:
            prefix = args.jdelim.join(self.tup) + args.jdelim
        else:
            prefix = ''

        if len(self.vals) > 1:
            v = corrcoef(self.vals, rowvar=0)
            for i,row in enumerate(v):
                for j in range(i):
                    args.outfile.write(prefix + args.jdelim.join((args.colNames[i], args.colNames[j], str(row[j]))) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute correlation of 2 or more columns')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default=[0,1])
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    args.outheader = Header()
    args.outheader.addCols(args.inheader.names(args.group))
    args.outheader.addCol('metric_1')
    args.outheader.addCol('metric_2')
    args.outheader.addCol('correlation')
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.colNames = args.inheader.names(args.columns)
    args.columns = args.inheader.indexes(args.columns)
    args.group = args.inheader.indexes(args.group)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, CorrelationGroup, args.group, args.delimiter, args.ordered)

