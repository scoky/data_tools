#!/usr/bin/python

import os
import sys
import argparse
import traceback
import scipy.stats as ss

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Generate samples from a given distribution')
    parser.add_argument('parameters', nargs='?', default="{}", help='dictionary of distribution parameters')
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-s', '--samples', type=int, default=1)
    parser.add_argument('-d', '--dist', default='norm')
    args = parser.parse_args()
    args.distf = getattr(ss, args.dist)
    args.parameters = eval(args.parameters)
    args.parameters["size"] = args.samples
    
    v = args.distf.rvs(**args.parameters)
    args.outfile.write('\n'.join(map(str, v)) + '\n')
