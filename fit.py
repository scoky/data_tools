#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper
import scipy.stats

class FitGroup(Group):
    def __init__(self, tup):
        super(FitGroup, self).__init__(tup)
        self.rows = [[] for i in args.columns]

    def add(self, chunks):
        vals = [float(findNumber(chunks[i])) for i in args.columns]
        for v,r in zip(vals, self.rows):
            r.append(v)

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        for c,r in zip(args.columns, self.rows):
            if len(self.tup) > 0:
                args.outfile.write(jdelim.join(self.tup) + jdelim)
            if len(args.columns) > 1:
                args.outfile.write(str(c) + jdelim)
            shape_params = args.distf.fit(r, **eval(args.parameters))
            ks_res = scipy.stats.kstest(r, args.dist, shape_params)
            args.outfile.write(jdelim.join(map(str, shape_params)) + jdelim + jdelim.join(map(str, ks_res)) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the distribution fit to column in the input')
    parser.add_argument('parameters', nargs='?', help='dictionary of fit parameters')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-i', '--dist', default='norm')    
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    args.distf = getattr(scipy.stats, args.dist)

    grouper = UnsortedInputGrouper(args.infile, FitGroup, args.group, args.delimiter)
    grouper.group()

