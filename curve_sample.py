#!/usr/bin/python

import os
import sys
import argparse
import traceback
from numpy import linspace
from input_handling import parseLines,findFloat

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Generate CDF of given distribution')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-b', '--begin', type=float, default=None)
    parser.add_argument('-e', '--end', type=float, default=None)
    parser.add_argument('-n', '--number', type=int, default=None)
    parser.add_argument('-s', '--source', default='scipy.stats', choices=['scipy.stats', 'builtin', 'lambda'], help='source of the curve to fit')
    parser.add_argument('-c', '--curve', default='paretoLomax')
    parser.add_argument('-p', '--params', default='', help='initial parameters')
    parser.add_argument('-x', '--xvalue', type=int, default=0)
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    
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
    
    if any( (args.begin, args.end, args.number) ):
        x = linspace(args.begin, args.end, args.number)
    else:
        x = (chunks[0] for chunks in parseLines(args.infile, args.delimiter, [args.xvalue], findFloat))
    for xx in x:
        args.outfile.write(str(xx) + ' ' + str(args.curvef(xx, *args.params)) + '\n')
