#!/usr/bin/env python

import os
import sys
import argparse
from collections import defaultdict
from data_tools.lib.files import ParameterParser,findNumber
from data_tools.lib.group import Group,run_grouping

class BinGroup(Group):
    def __init__(self, tup):
        super(BinGroup, self).__init__(tup)
        if args.numerical:
            tup = [findNumber(t) for t in tup]
        self.key = tuple([args.fuzz(t) for t in tup])

    def add(self, chunks):
        args.bins[self.key] += 1

    def done(self):
        pass

class SimilarGroup(Group):
    def __init__(self, tup):
        super(SimilarGroup, self).__init__(tup)
        if args.numerical:
            tup = [findNumber(t) for t in tup]
        self.key = tuple(self.tup)
        for k in args.bins:
            if args.similar(self.key, k):
                self.key = k
                break

    def add(self, chunks):
        args.bins[self.key] += 1

    def done(self):
        pass

# Default handling of input value
def nofuzz(v):
    return v

def bayesian_blocks(t):
    import numpy as np
    # copy and sort the array
    t = np.sort(t)
    N = t.size
    # create length-(N + 1) array of cell edges
    edges = np.concatenate([t[:1],
                            0.5 * (t[1:] + t[:-1]),
                            t[-1:]])
    block_length = t[-1] - edges
    # arrays needed for the iteration
    nn_vec = np.ones(N)
    best = np.zeros(N, dtype=float)
    last = np.zeros(N, dtype=int)
    #-----------------------------------------------------------------
    # Start with first data cell; add one cell at each iteration
    #-----------------------------------------------------------------
    for K in range(N):
        # Compute the width and count of the final bin for all possible
        # locations of the K^th changepoint
        width = block_length[:K + 1] - block_length[K + 1]
        count_vec = np.cumsum(nn_vec[:K + 1][::-1])[::-1]
        # evaluate fitness function for these possibilities
        fit_vec = count_vec * (np.log(count_vec) - np.log(width))
        fit_vec -= 4  # 4 comes from the prior on the number of changepoints
        fit_vec[1:] += best[:K]
        # find the max of the fitness: this is the K^th changepoint
        i_max = np.argmax(fit_vec)
        last[K] = i_max
        best[K] = fit_vec[i_max]
    #-----------------------------------------------------------------
    # Recover changepoints by iteratively peeling off the last block
    #-----------------------------------------------------------------
    change_points =  np.zeros(N, dtype=int)
    i_cp = N
    ind = N
    while True:
        i_cp -= 1
        change_points[i_cp] = ind
        if ind == 0:
            break
        ind = last[ind - 1]
    change_points = change_points[i_cp:]
    return edges[change_points]

if __name__ == "__main__":
    pp = ParameterParser('Compute bins', columns = 0, labels = [None], append = False)
    pp.parser.add_argument('-f', '--fuzz', default=None, help='lambda specifying fuzz for bins, e.g., "lambda x: x / 10"')
    pp.parser.add_argument('-s', '--similar', default=None, help='lambda specifying similarity between two arguments, e.g., "lambda x,y: abs(a - b) < 5"')
    pp.parser.add_argument('-m', '--method', default='bin', choices=['bin', 'similar', 'bayes'], help='')
    pp.parser.add_argument('-n', '--numerical', action='store_true', default=False, help='treat the group values as numbers')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = ['_'.join(args.group_names + ['bin'])]
    args = pp.getArgs(args)
    if all((args.similar, args.fuzz)):
        raise Exception('Cannot specify both fuzz and similar')
    if not args.fuzz:
        args.fuzz = nofuzz
        cls = BinGroup
    else:
        args.fuzz = eval(args.fuzz)
        cls = BinGroup
    if args.similar:
        args.similar = eval(args.similar)
        cls = SimilarGroup

    args.bins = defaultdict(int)
    run_grouping(args.infile, cls, args.group, args.ordered)
    for k,v in args.bins.items():
        args.outfile.write(list(k) + [v])
