#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping

class UniqueGroup(Group):
    def __init__(self, tup):
        super(UniqueGroup, self).__init__(tup)
        self.sets = set()

    def add(self, chunks):
        val = args.jdelim.join( (chunks[c] for c in args.columns) )
        self.sets.add(val)

    def done(self):
        if len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
        args.outfile.write(str(len(self.sets)) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute uniques counts of column(s)')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default=[0])
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
    args.outheader.addCol("_".join(args.inheader.names(args.columns)) + "_unique")
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.columns = args.inheader.indexes(args.columns)
    args.group = args.inheader.indexes(args.group)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, UniqueGroup, args.group, args.delimiter, args.ordered)
