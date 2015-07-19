#!/usr/bin/python

import os
import sys
import argparse
import traceback
from group import Group,run_grouping
from scipy import interpolate
import numpy as np

class ResampleGroup(Group):
    def __init__(self, tup):
        super(ResampleGroup, self).__init__(tup)
        self.xpoints = []
        self.ypoints = []

    def add(self, chunks):
        self.xpoints.append(float(chunks[args.xdata]))
        self.ypoints.append(float(chunks[args.ydata]))

    def done(self):
        fit = args.interpolatef(self.xpoints, self.ypoints)
        ynew = fit(args.xnew)
        
        prefix = ''
        if len(self.tup) > 0:
                prefix = args.jdelim.join(self.tup) + args.jdelim
        for x,y in zip(args.xnew, ynew):
            args.outfile.write(prefix + str(x) + args.jdelim + str(y) + '\n')
            
def interp_linear(x, y)
    return interp1d(x, x, kind=args.interpolate, copy=False)

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Resample the data points with a different frequency')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-i', '--interpolate', choices=['linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic', 'spline'], default='linear')
    parser.add_argument('-s', '--space', choices=['linear', 'log'], default='linear')
    parser.add_argument('-b', '--begin', type=float, default=None, help='value to begin resampling at')
    parser.add_argument('-t', '--terminate', type=float, default=None, help='value to terminate resampling at')
    parser.add_argument('-n', '--number', type=int, default=10, help='total number of data points to sample')
    parser.add_argument('-f', '--resample_file', type=argparse.FileType('r'), default=None, help='File to read resample points from')
    parser.add_argument('-r', '--resample_index', type=int, default=0)
    parser.add_argument('-x', '--xdata', type=int, default=0)
    parser.add_argument('-y', '--ydata', type=int, default=1)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.jdelim = args.delimiter if args.delimiter != None else ' '
    
    if args.interpolate == 'spline':
        args.interpolatef = interpolate.InterpolatedUnivariateSpline
    else:
        args.interpolatef = interp_linear
    
    if args.resample_file:
        args.xnew = []
        for line in args.resample_file:
            args.xnew.append(float(line.rstrip().split()[args.resample_index]))
        args.resample_file.close()
    elif args.space == 'linear':
        args.xnew = np.linspace(args.begin, args.terminate, args.number)
    else:
        args.xnew = np.logspace(args.begin, args.terminate, args.number)
    
    run_grouping(args.infile, ResampleGroup, args.group, args.delimiter, args.ordered)
