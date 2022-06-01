#!/usr/bin/env python

import os
import sys
import argparse
import traceback
import random
from bisect import bisect_left
from input_handling import parseLines,findFloat

class EmpiricalDistribution():
    @classmethod
    def fromFile(cls, infile):
        dist = EmpiricalDistribution([], [])
        for line in infile:
            x,y = line.rstrip().split()
            dist.x.append(float(x))
            dist.y.append(float(y))
        return dist

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def f_x(self, y):
        return self.find(self.y, self.x, y)
    
    def find(self, col1, col2, col1_val):
        index = bisect_left(col1, col1_val)
        if index == len(col1):
            return col2[index-1]
        if index == 0 or col1_val == col1[index]:
            return col2[index]
        else: # Use linear interpolation
            return col2[index-1] + (col2[index] - col2[index-1]) * (col1_val - col1[index-1]) / (col1[index] - col1[index-1])
            
    def f_y(self, x):
        return self.find(self.x, self.y, x)

def empirical_sample():
    return args.empirical.f_x(random.random())

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Sample from a given distribution')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-n', '--number', type=int, default=None)
    parser.add_argument('-s', '--source', default='scipy.stats', choices=['scipy.stats', 'builtin', 'lambda'], help='source of the curve to fit')
    parser.add_argument('-c', '--curve', default='paretoLomax')
    parser.add_argument('-p', '--params', default='', help='initial parameters')
    parser.add_argument('-e', '--seed', type=int, default=None, help='the seed value for random number generation')
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    random.seed(args.seed)

    args.params = list(map(float, args.params.split()))

    if args.source == 'scipy.stats':
        import scipy.stats as ss
        args.source = ss
    elif args.source == 'builtin':
        from . import curve_fit
        args.source = curve_fit
    else:
        args.source = None

    if args.curve == 'empirical':
        args.curvef = empirical_sample
        args.empirical = EmpiricalDistribution.fromFile(args.infile)
    elif args.source:
        mod = args.source
        for c in args.curve.split('.'):
            mod = getattr(mod, c)
        args.curvef = mod
    else:
        args.curvef = eval(args.curve)

    for x in range(args.number):
        args.outfile.write(str(args.curvef(*args.params)) + '\n')

