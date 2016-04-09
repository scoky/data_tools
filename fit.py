#!/usr/bin/env python

import os
import sys
import argparse
import scipy.stats
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping

DIST = [ "all", "alpha", "anglit", "arcsine", "beta", "betaprime", "bradford", "burr", "cauchy", "chi", "chi2", "cosine", 
    "dgamma", "dweibull", "erlang", "expon", "exponnorm", "exponweib", "exponpow", "f", "fatiguelife", "fisk", 
    "foldcauchy", "foldnorm", "frechet_r", "frechet_l", "genlogistic", "gennorm", "genpareto", "genexpon", 
    "genextreme", "gausshyper", "gamma", "gengamma", "genhalflogistic", "gilbrat", "gompertz", "gumbel_r", 
    "gumbel_l", "halfcauchy", "halflogistic", "halfnorm", "halfgennorm", "hypsecant", "invgamma", "invgauss", 
    "invweibull", "johnsonsb", "johnsonsu", "ksone", "kstwobign", "laplace", "levy", "levy_l", "levy_stable", 
    "logistic", "loggamma", "loglaplace", "lognorm", "lomax", "maxwell", "mielke", "nakagami", "ncx2", "ncf", 
    "nct", "norm", "pareto", "pearson3", "powerlaw", "powerlognorm", "powernorm", "rdist", "reciprocal", "rayleigh", 
    "rice", "recipinvgauss", "semicircular", "t", "triang", "truncexpon", "truncnorm", "tukeylambda", "uniform", 
    "vonmises", "vonmises_line", "wald", "weibull_min", "weibull_max", "wrapcauchy", "multivariate_normal", 
    "matrix_normal", "dirichlet", "wishart", "invwishart", "bernoulli", "binom", "boltzmann", "dlaplace", "geom", 
    "hypergeom", "logser", "nbinom", "planck", "poisson", "randint", "skellam", "zipf" ]

class FitGroup(Group):
    def __init__(self, tup):
        super(FitGroup, self).__init__(tup)
        self.row = []

    def add(self, chunks):
        val = float(findNumber(chunks[args.column]))
        self.row.append(val)

    def done(self):
        for dist,i in zip(args.dist, args.distf):
            if len(self.tup) > 0:
                args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
            shape_params = i.fit(self.rows, **eval(args.parameters))
            ks_res = scipy.stats.kstest(r, dist, shape_params)
            args.outfile.write(dist + jdelim + jdelim.join(map(str, shape_params)) + jdelim + jdelim.join(map(str, ks_res)) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the distribution fit to column in the input')
    parser.add_argument('parameters', nargs='?', default="{}", help='dictionary of fit parameters')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', default=0)
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-i', '--dist', nargs='+', default=['norm'], choices=DIST)
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.distf = []
    if 'all' in args.dist:
        args.dist.remove('all')
        args.dist.extend(DIST)
    for i in args.dist:
        args.distf.append(getattr(scipy.stats, i))
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    args.outheader = Header()
    args.outheader.addCols(args.inheader.names(args.group))
    args.outheader.addCol('_'.join(args.inheader.names(args.group)) + '_count')
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.group = args.inheader.indexes(args.group)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, FitGroup, args.group, args.delimiter, args.ordered)

