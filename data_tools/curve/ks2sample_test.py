#!/usr/bin/env python

import os
import sys
import argparse
import traceback
import random
sys.path.insert(1, os.path.join(os.path.dirname(__file__), os.pardir))
from toollib.group import Group,run_grouping
from toollib.files import ParameterParser,findNumber
from scipy.stats import ks_2samp

class KSGroup(Group):
    def __init__(self, tup):
        super(KSGroup, self).__init__(tup)
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

def KS_test(groups, outfile):
    jdelim = args.delimiter if args.delimiter != None else ' '
    for i,u in enumerate(groups):
        for j,v in enumerate(groups):
            if j > i or (j == i and len(args.columns) == 1):
                break
            for x,us in enumerate(u.samples):
                for y,vs in enumerate(v.samples):
                    if j == i and y >= x:
                        break
                    if args.random != None:
                        verdict = False
                        for k in range(args.random):
                            res = ks_2samp(random.sample(us, args.subsample), random.sample(vs, args.subsample))
                            if res[0] < res[1]:
                                verdict = True
                            outfile.write([jdelim.join(u.tup + v.tup + list(map(str, res))) + '\n'])
                        outfile.write(['Verdict:' + str(verdict) + '\n'])
                    else:
                        res = ks_2samp(us, vs)
                        verdict = False
                        if res[0] < res[1]:
                            verdict = True
                        outfile.write([jdelim.join(u.tup + v.tup + list(map(str, res))) + '\n'])
                        outfile.write(['Verdict:' + str(verdict) + '\n'])

if __name__ == "__main__":
    # set up command line args
    pp = ParameterParser('Compute KS 2-sample', infiles = '*', columns = '*', append = False, labels = [None])
    pp.parser.add_argument('-r', '--random', default=None, type=int, help='perform on r random subsamples')
    pp.parser.add_argument('-s', '--subsample', default=100, type=int, help='subsample size')
    args = pp.parseArgs()
    args = pp.getArgs(args)

    args.groups = []
    for infile in args.infiles:
        run_grouping(infile, KSGroup, args.group, args.delimiter)
    KS_test(args.groups, args.outfile)
