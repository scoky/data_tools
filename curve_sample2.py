#!/usr/bin/python

import os
import sys
import argparse
import traceback
import random
from numpy import linspace
from input_handling import parseLines,findFloat

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

    args.params = map(float, args.params.split())

    if args.source == 'scipy.stats':
        import scipy.stats as ss
        args.source = ss
    elif args.source == 'builtin':
        import curve_fit
        args.source = curve_fit
    else:
        args.source = None

    if args.source:
        mod = args.source
        for c in args.curve.split('.'):
            mod = getattr(mod, c)
        args.curvef = mod
    else:
        args.curvef = eval(args.curve)

    for x in xrange(args.number):
        args.outfile.write(str(args.curvef(*args.params)) + '\n')

