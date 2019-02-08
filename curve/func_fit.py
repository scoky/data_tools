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
        from scipy.optimize import curve_fit
        popt, pcov = curve_fit(args.function, x, y)
        sys.stderr.write('{0} {1}\n'.format(popt, pcov))
        if args.range is None:
            x = np.linspace(x[0], x[-1], args.granularity)
        else:
            x = np.linspace(args.range[0], args.range[-1], args.granularity)
        y = args.function(x, *popt)
        for xi,yi in zip(x,y):
            args.outfile.write(self.tup + [xi, yi])

if __name__ == "__main__":
    # set up command line args
    pp = ParameterParser('Compute polynomial to fit data', columns = 0, labels = [None], append = False)
    pp.parser.add_argument('-x', default = 0)
    pp.parser.add_argument('-y', default = 1)
    pp.parser.add_argument('-f', '--function', required = True, help = 'lambda expression of function to fit')
    pp.parser.add_argument('-r', '--range', nargs = 2, default = None, type = int)
    pp.parser.add_argument('-a', '--granularity', default = 1000, type = int)
    args = pp.parseArgs()
    args = pp.getArgs(args)
    args.x = args.infile.header.index(args.x)
    args.y = args.infile.header.index(args.y)
    import numpy as np
    args.function = eval(args.function)

    run_grouping(args.infile, FitGroup, args.group, args.ordered)
