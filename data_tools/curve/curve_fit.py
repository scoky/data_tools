#!/usr/bin/env python

import os
import sys
import argparse
import traceback
import numpy as np
from math import factorial
from group import Group,UnsortedInputGrouper
from scipy.optimize import curve_fit as cfit
import scipy.stats as ss
#import scipy.special

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

#def zipf(xdata, a):
#    return np.power(xdata, -a)/scipy.special.zetac(a)

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
            try:
                pvar = np.diag(pcov)
            except:
                pvar = [None]
            args.outfile.write(jdelim.join(map(str, popt)) + jdelim + curve + jdelim + jdelim.join(map(str, pvar)) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the curve fit to column in the input')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-s', '--source', default='scipy.stats', choices=['scipy.stats', 'builtin', 'lambda'], help='source of the curve to fit')
    parser.add_argument('-c', '--curve', nargs='+', default=['pareto'], help='one of the built in curves or a lambda expression')
    parser.add_argument('-p', '--params', default='', help='initial parameters')
    parser.add_argument('-x', '--xdata', type=int, default=0)
    parser.add_argument('-y', '--ydata', type=int, default=1)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    if args.source == 'scipy.stats':
        args.source = ss
    elif args.source == 'builtin':
        args.source = sys.modules[__name__]
    else:
        args.source = None
        
    args.params = list(map(float, args.params.split(args.delimiter)))
        
    args.curvef = []
    for i in args.curve:
        if args.source:
            mod = args.source
            for c in i.split('.'):
                mod = getattr(mod, c)
            args.curvef.append(mod)
        else:
            args.curvef.append(eval(i))

    grouper = UnsortedInputGrouper(args.infile, FitGroup, args.group, args.delimiter)
    grouper.group()

