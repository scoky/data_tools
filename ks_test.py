#!/usr/bin/python

import os
import sys
import argparse
import traceback
from group import Group,UnsortedInputGrouper
import scipy.stats as ss

class KSGroup(Group):
    def __init__(self, tup):
        super(KSGroup, self).__init__(tup)
        self.samples = []

    def add(self, chunks):
        self.samples.append(float(chunks[args.column]))

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        if len(self.tup) > 0:
            args.outfile.write(jdelim.join(self.tup) + jdelim)
        args.outfile.write(jdelim.join(map(str, ss.kstest(self.samples, args.distf, args=args.params))) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compare the request distributions of all clients')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-s', '--source', default='scipy.stats', choices=['scipy.stats', 'lambda'], help='source of the distribution to fit')
    parser.add_argument('-i', '--dist', default='paretoLomax')
    parser.add_argument('-p', '--params', nargs='+', type=float, default=[], help='initial parameters')
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    if args.source == 'scipy.stats':
        args.source = ss
    else:
        args.source = None
        
    if args.source:
        mod = args.source
        for c in args.dist.split('.'):
            mod = getattr(mod, c)
        args.distf = mod.cdf
    else:
        args.distf = eval(args.dist)

    grouper = UnsortedInputGrouper(args.infile, KSGroup, args.group, args.delimiter)
    grouper.group()
