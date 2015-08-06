#!/usr/bin/python

import os
import sys
import argparse
import traceback
import random
from group import Group,UnsortedInputGrouper
from scipy.stats import anderson_ksamp

confidence = [25, 10, 5, 2.5, 1]

class ADGroup(Group):
    def __init__(self, tup):
        super(ADGroup, self).__init__(tup)
        args.groups.append(self)
        self.samples = []

    def add(self, chunks):
        self.samples.append(float(chunks[args.column]))

    def done(self):
        pass

def AD_test(groups, outfile):
    jdelim = args.delimiter if args.delimiter != None else ' '
    for i,u in enumerate(groups):
        if len(u.samples) < args.ignore:
            continue
        for j,v in enumerate(groups):
            if j >= i:
                break
            if len(v.samples) < args.ignore:
                continue
            if args.random != None:
                verdict = False
                for k in range(args.random):
                    res = anderson_ksamp([random.sample(u.samples, args.subsample), random.sample(v.samples, args.subsample)])
                    if res[0] < res[1][0]:
                        verdict = True
                    outfile.write(jdelim.join(u.tup + v.tup + map(str, res)) + '\n')
                outfile.write('Verdict:' + str(verdict) + '\n')
            else:
                res = anderson_ksamp([u.samples, v.samples])
                verdict = False
                if res[0] < res[1][0]:
                        verdict = True
                outfile.write(jdelim.join(u.tup + v.tup + map(str, res)) + '\n')
                outfile.write('Verdict:' + str(verdict) + '\n')

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
    parser.add_argument('-r', '--random', default=None, type=int, help='perform on r random subsamples')
    parser.add_argument('-s', '--subsample', default=100, type=int, help='subsample size')
    args = parser.parse_args()

    args.groups = []
    grouper = UnsortedInputGrouper(args.infile, ADGroup, args.group, args.delimiter)
    grouper.group()
    AD_test(args.groups, args.outfile)
