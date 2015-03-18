#!/usr/bin/python

import os
import sys
import argparse
import traceback
import numpy as np
from math import factorial
from group import Group,UnsortedInputGrouper
from scipy.optimize import curve_fit as cfit

def first_degree(xdata, a, b):
    return a * xdata + b

def second_degree(xdata, a, b, c):
    return a * np.power(xdata, 2) + b * xdata + c
    
def third_degree(xdata, a, b, c, d):
    return a * np.power(xdata, 3) + b * np.power(xdata, 2) + c * xdata + d
    
def fourth_degree(xdata, a, b, c, d, e):
    return a * np.power(xdata, 4) + b * np.power(xdata, 3) + c * np.power(xdata, 2) + d * xdata + e
    
def gamma(xdata, k, theta):
    return np.power(xdata, k-1) * np.exp(xdata / -theta) / ( np.power(theta, k) * factorial(k-1) )
    
def paretoI(xdata, xm, a):
    return a * np.power(xm, a) / np.power(xdata, a+1)
    
def paretoLomax(xdata, l, a):
    return a * np.power(l, a) / np.power(xdata+l, a+1)
    
def paretoLomaxCDF(xdata, l, a):
    return 1 - np.power(1 + xdata/l, -a)
    
def pareto(xdata, shape, location, scale):
    return np.power(1 + shape * (xdata - location) / scale, -1 / (shape+1)) / scale
    
def paretoCDF(xdata, shape, location, scale):
    return 1 - np.power(1 + shape * (xdata - location) / scale, -1 / shape)

class FitGroup(Group):
    def __init__(self, tup):
        super(FitGroup, self).__init__(tup)
        self.xdata = []
        self.ydata = []

    def add(self, chunks):
        self.xdata.append(float(chunks[args.xdata]))
        self.ydata.append(float(chunks[args.ydata]))

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        for curve,i in zip(args.curve, args.curvef):
            if len(self.tup) > 0:
                args.outfile.write(jdelim.join(self.tup) + jdelim)
            popt, pcov = cfit(i, self.xdata, self.ydata, p0=args.params)
            perr = np.sqrt(np.diag(pcov))
            args.outfile.write(jdelim.join(map(str, popt)) + jdelim + curve + jdelim + jdelim.join(map(str, perr)) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the curve fit to column in the input')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--curve', nargs='+', default=['paretoLomax'], help='one of the built in curves or a lambda expression')
    parser.add_argument('-p', '--params', nargs='+', type=float, default=None, help='initial parameters')
    parser.add_argument('-x', '--xdata', type=int, default=0)
    parser.add_argument('-y', '--ydata', type=int, default=1)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    args.curvef = []
    for i in args.curve:
        args.curvef.append(getattr(sys.modules[__name__], i))

    grouper = UnsortedInputGrouper(args.infile, FitGroup, args.group, args.delimiter)
    grouper.group()

