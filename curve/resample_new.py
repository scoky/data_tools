#!/usr/bin/env python

import os
import sys
import argparse
sys.path.insert(1, os.path.join(os.path.dirname(__file__), os.pardir))
from toollib.group import Group,run_grouping
from toollib.files import ParameterParser,findNumber

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
        for x,y in zip(args.xnew, ynew):
            args.outfile.write(self.tup + [x, y])
            
def interp_linear(x, y):
    from scipy import interpolate
    return interpolate.interp1d(x, y, kind=args.interpolate, copy=False)

if __name__ == "__main__":
    pp = ParameterParser('Resample the data points with a different frequency', infiles = 1, columns = 0, append = False, labels = [None])
    pp.parser.add_argument('-i', '--interpolate', choices=['linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic', 'spline'], default='linear')
    pp.parser.add_argument('-s', '--space', choices=['linear', 'log'], default='linear')
    pp.parser.add_argument('-b', '--begin', type=float, default=None, help='value to begin resampling at')
    pp.parser.add_argument('-t', '--terminate', type=float, default=None, help='value to terminate resampling at')
    pp.parser.add_argument('-n', '--number', type=int, default=10, help='total number of data points to sample')
    pp.parser.add_argument('-f', '--resample_file', default=None, help='File to read resample points from')
    pp.parser.add_argument('-r', '--resample_index', default=0)
    pp.parser.add_argument('-x', '--xdata', default=0)
    pp.parser.add_argument('-y', '--ydata', default=1)
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = ['x', 'y']
    args = pp.getArgs(args)
    args.xdata = args.infile.header.index(args.xdata)
    args.ydata = args.infile.header.index(args.ydata)
    from scipy import interpolate
    import numpy as np

    if args.interpolate == 'spline':
        args.interpolatef = interpolate.InterpolatedUnivariateSpline
    else:
        args.interpolatef = interp_linear
    
    if args.resample_file:
        args.xnew = []
        with FileReader(args.resample_file, args) as f:
            for chunks in f:
                args.xnew.append(float(chunks[args.resample_index]))
    elif args.space == 'linear':
        args.xnew = np.linspace(args.begin, args.terminate, args.number)
    else:
        args.xnew = np.logspace(args.begin, args.terminate, args.number)
    
    run_grouping(args.infile, ResampleGroup, args.group, args.ordered)
