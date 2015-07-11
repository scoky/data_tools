#!/usr/bin/python

import os
import sys
import argparse
import traceback
from group import Group,UnsortedInputGrouper
from numpy import corrcoef

class CorrelationGroup(Group):
    def __init__(self, tup):
        super(CorrelationGroup, self).__init__(tup)
        self.vals = []

    def add(self, chunks):
        self.vals.append([float(chunks[i]) for i in args.columns])

    def done(self):
        if len(self.tup) > 0:
            prefix = args.jdelim.join(self.tup) + args.jdelim
        else:
            prefix = ''

        v = corrcoef(self.vals, rowvar=0)
        args.outfile.write(prefix + str(v) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute correlation of 2 or more columns')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0,1])
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    args.jdelim = args.delimiter if args.delimiter != None else ' '
    
    grouper = UnsortedInputGrouper(args.infile, CorrelationGroup, args.group, args.delimiter)
    grouper.group()
