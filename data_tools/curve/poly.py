#!/usr/bin/env python

import os
import sys
import argparse
sys.path.insert(1, os.path.join(os.path.dirname(__file__), os.pardir))
from toollib.files import findNumber,ParameterParser
from toollib.group import Group,run_grouping

class FitGroup(Group):
    def __init__(self, tup):
        super(FitGroup, self).__init__(tup)
        self.d = []

    def add(self, chunks):
        self.d.append((float(findNumber(chunks[args.x])), float(findNumber(chunks[args.y]))))

    def done(self):
        import numpy as np
        d = np.array(sorted(self.d, key = lambda x: x[0]))
        x = d[:,0]
        y = d[:,1]
        z = np.polyfit(x, y, args.degree)
        f = np.poly1d(z)
        formula = 'f(x) = ' + ' + '.join('({0} * x^{1})'.format(zi, args.degree - i) for i,zi in enumerate(z))
        sys.stderr.write(formula + '\n')
        if args.range is None:
            x = np.linspace(x[0], x[-1], args.granularity)
        else:
            x = np.linspace(args.range[0], args.range[-1], args.granularity)
        y = f(x)
        for xi,yi in zip(x,y):
            args.outfile.write(self.tup + [xi, yi])

if __name__ == "__main__":
    # set up command line args
    pp = ParameterParser('Compute polynomial to fit data', columns = 0, labels = [None], append = False)
    pp.parser.add_argument('-x', default = 0)
    pp.parser.add_argument('-y', default = 1)
    pp.parser.add_argument('-d', '--degree', default = 2, type = int)
    pp.parser.add_argument('-r', '--range', nargs = 2, default = None, type = int)
    pp.parser.add_argument('-a', '--granularity', default = 1000, type = int)
    args = pp.parseArgs()
    args = pp.getArgs(args)
    args.x = args.infile.header.index(args.x)
    args.y = args.infile.header.index(args.y)

    run_grouping(args.infile, FitGroup, args.group, args.ordered)
