#!/usr/bin/env python

import os
import sys
import argparse
sys.path.insert(1, os.path.join(os.path.dirname(__file__), os.pardir))
from toollib.files import findNumber,ParameterParser
from toollib.group import Group,run_grouping
import numpy as np
from collections import namedtuple

class KernelStatistic:
    def __init__(self, h_range = None):
        # Gretton, A., Fukumizu, K., Harchaoui, Z., & Sriperumbudur, B. K. (2009). A fast, consistent kernel two-sample test. In Advances in neural information processing systems (pp. 673-681).
        self.h_range = np.linspace(0.01, 100, 1000) if h_range is None else h_range

    def T(self, X, Y):
        # sup(T_h) h > 0
        m = None
        h_i = None
        t_p = None
        for h in self.h_range: # introduce some discreteness
            t = self.T_h(X, Y, h)
            if m is None or t > m:
                m = t
                h_i = h
            if t_p is not None and t < t_p: # Curve has only 1 maximum (i.e., convex), so we can break when slope is negative
                break
            t_p = t
        return m, h_i

    @classmethod
    def K_h(cls, X, Y, h):
        return np.exp(-np.square(np.linalg.norm(np.reshape(X[:, None] - Y, (len(X) * len(Y), -1)), axis = 1)) / np.square(h))

    @classmethod
    def T_h(cls, X, Y, h):
        s1 = np.sum(cls.K_h(X, X, h)) / np.square(len(X))
        s2 = (2 * np.sum(cls.K_h(X, Y, h))) / (len(X) * len(Y))
        s3 = np.sum(cls.K_h(Y, Y, h)) / np.square(len(Y))
        return s1 - s2 + s3

Result = namedtuple('Result', ['pvalue', 'statistic', 'h_0', 't_mean', 't_std', 'h_mean', 'h_std'])

class Permuter:
    def __init__(self, N = 1000, statistic = KernelStatistic()):
        # See: https://normaldeviate.wordpress.com/2012/07/14/modern-two-sample-tests/
        self.N = N
        self.stat = statistic

    def run(self, X, Y):
        t_x, h_x = self.stat.T(X, Y)
        union = np.concatenate((X, Y), axis = 0)
        count = 0
        # p = (1/N)sum(I(T_j > T))
        m = []
        h = []
        for n in range(self.N):
            np.random.shuffle(union) # Randomly re-assign samples to X and Y
            t_j, h_j = self.stat.T(union[:len(X)], union[len(X):])
            m.append(t_j)
            h.append(h_j)
            if t_j > t_x:
                count += 1
        p = float(count) / self.N
        return Result(p, t_x, h_x, np.mean(m), np.std(m), np.mean(h), np.std(h))

if __name__ == "__main__":
    pp = ParameterParser('Permutation method for 2 sample null hypothesis testing', columns = '*', infiles = 2, group = False, ordered = False, append = False)
    pp.parser.add_argument('-n', '--n', type = int, default = 1000)
    pp.parser.add_argument('-s', '--statistic', default = 'kernel', choices= ['kernel'])
    pp.parser.add_argument('--h_range', nargs = 3, type = float, default = [0.01, 100, 1000], help = 'linear space from arg1 to arg2 of arg3 steps')
    args = pp.parseArgs()
    args = pp.getArgs(args)

    if args.statistic == 'kernel':
        stat = KernelStatistic(h_range = np.linspace(*args.h_range))
    p = Permuter(N = args.n, statistic = stat)
    inputs = []
    for infile in args.infiles:
        Y = []
        for line in infile:
            Y.append([float(findNumber(chunks[i])) for i in args.columns])
        y = np.array(Y)
        for X in inputs:
            print(p.run(X, Y))
        inputs.append(Y)
