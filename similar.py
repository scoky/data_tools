#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper

class SimilarGroup(Group):
    def __init__(self, tup):
        super(SimilarGroup, self).__init__(tup)
        self.bins = []
        for c in args.columns:
            self.bins.append({})

    def add(self, chunks):
        vals = [chunks[i] for i in args.columns]
        for v,b in zip(vals, self.bins):
            found = False
            for k in b:
                if args.similar(v, k):
                    b[k] += 1
                    found = True
                    break
            if not found:
                b[v] = 1

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        for c,b in zip(args.columns, self.bins):
            for k,v in b.iteritems():
                if len(self.tup) > 0:
                    args.outfile.write(jdelim.join(self.tup) + jdelim)
                if len(args.columns) > 1:
                    args.outfile.write(str(c) + jdelim)
                args.outfile.write(jdelim.join(map(str, [k, v])) + '\n')
            
# Default handling of input value    
def nofuzz(v,u):
    return v==u

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute similarity from column(s)')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-s', '--similar', default=None, help='lambda specifying how to determine similarity between two arguments')
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    if not args.similar:
        args.similar = nofuzz
    else:
        args.similar = eval(args.similar)

    grouper = UnsortedInputGrouper(args.infile, SimilarGroup, args.group, args.delimiter)
    grouper.group()
