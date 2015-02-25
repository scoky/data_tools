#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper
from collections import defaultdict

class BinGroup(Group):
    def __init__(self, tup):
        super(BinGroup, self).__init__(tup)
        self.bins = []
        for c in args.columns:
            self.bins.append(defaultdict(int))

    def add(self, chunks):
        vals = [args.fuzzy(chunks[i]) for i in args.columns]
        for v,b in zip(vals, self.bins):
            b[v] += 1

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        for c,b in zip(args.columns, self.bins):
            for k,v in b.iteritems():
                if len(self.tup) > 0:
                    args.outfile.write(jdelim.join(self.tup) + jdelim)
                args.outfile.write(jdelim.join(map(str, [c, k, v])) + '\n')
            
# Default handling of input value    
def nofuzz(v):
    return v

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute bins from column(s)')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-f', '--fuzzy', default=None, help='lambda specifying how to fuzz bins')
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    if not args.fuzzy:
        args.fuzzy = nofuzz
    else:
        args.fuzzy = eval(args.fuzzy)

    grouper = UnsortedInputGrouper(args.infile, BinGroup, args.group, args.delimiter)
    grouper.group()
