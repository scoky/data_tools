#!/usr/bin/python

import os
import sys
import argparse
import traceback
import scipy.stats as ss
from numpy import linspace

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the residual of input samples with a fitted distribution')
    parser.add_argument('parameters', nargs='*', type=float, default=[], help='distribution parameters')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-d', '--dist', default='norm')
    args = parser.parse_args()
    args.distf = getattr(ss, args.dist)

    for line in args.infile:
        x,y = line.rstrip().split()
        delta = float(y) - args.distf.cdf(float(x), *args.parameters)
        args.outfile.write(str(delta) + '\n')