#!/usr/bin/python

import os
import sys
import argparse
import traceback
from group import Group,UnsortedInputGrouper
from scipy import stats

class KSGroup(Group):
    def __init__(self, tup):
        super(KSGroup, self).__init__(tup)
        args.groups.append(self)
        self.samples = []

    def add(self, chunks):
        self.samples.append(float(chunks[args.column]))

    def done(self):
        pass

def KS_test(groups, outfile):
    jdelim = args.delimiter if args.delimiter != None else ' '
    for i,u in enumerate(groups):
        if len(u.samples) < args.ignore:
            continue
        for j,v in enumerate(groups):
            if j >= i:
                break
            if len(v.samples) < args.ignore:
                continue
            outfile.write(jdelim.join(u.tup + v.tup + map(str, stats.ks_2samp(u.samples, v.samples))) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compare the request distributions of all clients')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-i', '--ignore', type=int, default=0, help='filter groups with less than threshold number of samples')
    parser.add_argument('-c', '--column', type=int, default=1)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[0])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()

    args.groups = []
    grouper = UnsortedInputGrouper(args.infile, KSGroup, args.group, args.delimiter)
    grouper.group()
    KS_test(args.groups, args.outfile)
