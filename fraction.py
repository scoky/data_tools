#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping

class FractionGroup(Group):
    def __init__(self, tup):
        super(FractionGroup, self).__init__(tup)
        self.rows = []
        if args.append:
            self.add = self.addFull
            self.done = self.doneFull
        else:
            self.add = self.addCol
            self.done = self.doneCol

    def addFull(self, chunks):
        chunks.append(findNumber(chunks[args.column]))
        self.rows.append(chunks)
        
    def addCol(self, chunks):
        self.rows.append(findNumber(chunks[args.column]))

    def doneFull(self):
        total = sum(r[-1] for r in self.rows)
        for r in self.rows:
            r[-1] = str(r[-1] / total)
            args.outfile.write(args.jdelim.join(r) + '\n')

    def doneCol(self):
        prefix = ''
        if len(self.tup) > 0:
            prefix = args.jdelim.join(self.tup) + args.jdelim
        total = sum(self.rows)
        for r in self.rows:
            args.outfile.write(prefix + str(r / total) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute fraction from column(s)')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', default=0)
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-d', '--delimiter', default=None)
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
    args.outheader.addCol(args.inheader.name(args.column) + '_fraction')
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.column = args.inheader.index(args.column)
    args.group = args.inheader.indexes(args.group)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, FractionGroup, args.group, args.delimiter, args.ordered)

