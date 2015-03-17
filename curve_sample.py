#!/usr/bin/python

import os
import sys
import argparse
import traceback
from numpy import linspace
import curve_fit

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Generate CDF of given distribution')
    parser.add_argument('parameters', nargs='*', type=float, default=[], help='distribution parameters')
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-s', '--start', type=float, default=0)
    parser.add_argument('-e', '--end', type=float, default=1)
    parser.add_argument('-n', '--number', type=int, default=100)
    parser.add_argument('-c', '--curve', default='paretoLomax')
    args = parser.parse_args()
    args.curvef = getattr(curve_fit, args.curve)
    
    x = linspace(args.start, args.end, args.number)
    y = args.curvef(x, *args.parameters)
    for xx,yy in zip(x,y):
        args.outfile.write(str(xx) + ' ' + str(yy) + '\n')
