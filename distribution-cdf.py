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
                                     description='Generate CDF of given distribution')
    parser.add_argument('parameters', nargs='?', default="{}", help='dictionary of distribution parameters')
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-s', '--start', type=float, default=0)
    parser.add_argument('-e', '--end', type=float, default=1)
    parser.add_argument('-n', '--number', type=int, default=100)
    parser.add_argument('-d', '--dist', default='norm')
    args = parser.parse_args()
    args.distf = getattr(ss, args.dist)
    args.parameters = eval(args.parameters)
    
    x = linspace(args.start, args.end, args.number)
    y = args.distf.cdf(x, **args.parameters)
    for xx,yy in zip(x,y):
        args.outfile.write(str(xx) + ' ' + str(yy) + '\n')
