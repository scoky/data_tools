#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper

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
        jdelim = args.delimiter if args.delimiter != None else ' '
        if len(self.tup) > 0:
            args.outfile.write(jdelim.join(self.tup) + jdelim)
        args.outfile.write(jdelim.join(map(str, [s/c for s,c in zip(self.sums, self.count)])) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute mean of column(s)')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-b', '--bins', nargs='+', type=int, default=[])
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()

    grouper = UnsortedInputGrouper(args.infile, MeanGroup, args.group, args.delimiter)
    grouper.group()
