#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping

class MeanGroup(Group):
    def __init__(self, tup):
        super(MeanGroup, self).__init__(tup)
        self.sums = [0]*len(args.columns)
        self.count = [0]*len(args.columns)
        self.add = self.addBin if len(args.bins) > 0 else self.addVal

    def addVal(self, chunks):
        vals = [findNumber(chunks[i]) for i in args.columns]
        self.sums[:] = [v+s for v,s in zip(vals, self.sums)]
        self.count[:] = [c+1 for c in self.count]
        
    def addBin(self, chunks):
        vals = [findNumber(chunks[i]) for i in args.columns]
        bins = [findNumber(chunks[i]) for i in args.bins]
        self.sums[:] = [(b*v)+s for v,s,b in zip(vals, self.sums, bins)]
        self.count[:] = [c+b for c,b in zip(self.count, bins)]

    def done(self):
        if len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
        args.outfile.write(args.jdelim.join(map(str, [s/c for s,c in zip(self.sums, self.count)])) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute mean of column(s)')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default=[0])
    parser.add_argument('-b', '--bins', nargs='+', default=[])
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
    args.outheader.addCols([col+'_mean' for col in args.inheader.names(args.columns)])
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.columns = args.inheader.indexes(args.columns)
    args.group = args.inheader.indexes(args.group)
    args.bins = args.inheader.indexes(args.bins)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, MeanGroup, args.group, args.delimiter, args.ordered)
