#!/usr/bin/env python

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
        for i in range(len(args.columns)):
            self.samples.append([])

    def add(self, chunks):
        values = [float(chunks[i]) for i in args.columns]
        for s,v in zip(self.samples, values):
            s.append(v)

    def done(self):
        pass

def AD_test(groups, outfile):
    jdelim = args.delimiter if args.delimiter != None else ' '
    for i,u in enumerate(groups):
        for j,v in enumerate(groups):
            if j > i or (j == i and len(args.columns) == 1):
                break
            for x,us in enumerate(u.samples):
                for y,vs in enumerate(v.samples):
                    if len(vs) < args.ignore or len(us) < args.ignore:
                        continue
                    if j == i and y >= x:
                        break
                    if args.random != None:
                        verdict = False
                        for k in range(args.random):
                            res = anderson_ksamp([random.sample(us, args.subsample), random.sample(vs, args.subsample)])
                            if res[0] < res[1][0]:
                                verdict = True
                            outfile.write(jdelim.join(u.tup + v.tup + map(str, res)) + '\n')
                        outfile.write('Verdict:' + str(verdict) + '\n')
                    else:
                        res = anderson_ksamp([us, vs])
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
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[1])
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-r', '--random', default=None, type=int, help='perform on r random subsamples')
    parser.add_argument('-s', '--subsample', default=100, type=int, help='subsample size')
    args = parser.parse_args()

    args.groups = []
    grouper = UnsortedInputGrouper(args.infile, ADGroup, args.group, args.delimiter)
    grouper.group()
    AD_test(args.groups, args.outfile)
