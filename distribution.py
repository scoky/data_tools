#!/usr/bin/python

import os
import sys
import argparse
import traceback
import random

DISTS = ['random', 'uniform', 'triangular', 'betavariate', 'expovariate', 'gammavariate',\
         'gauss', 'lognormvariate', 'normalvariate', 'vonmisesvariate', 'paretovariate',\
         'weibullvariate', 'WichmannHill']

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Generate random samples')
    parser.add_argument('parameters', nargs='+', type=float)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-s', '--samples', type=int, default=1)
    parser.add_argument('-d', '--dist', default='gauss', choices=DISTS)
    args = parser.parse_args()
    args.dist = getattr(random, args.dist)
        
    for i in range(args.samples):
        s = args.dist(*args.parameters)
        args.outfile.write(str(s) + '\n')
