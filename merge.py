#!/usr/bin/python

import os
import sys
import argparse
import traceback
from collections import defaultdict

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Merge files on column(s)')
    parser.add_argument('infiles', nargs='*', type=argparse.FileType('r'), default=[sys.stdin])
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-i', '--inner', action='store_true', default=False, help='inner merge')
    args = parser.parse_args()
    if len(args.columns) == 1:
        args.columns = args.columns*len(args.infiles)
    if len(args.columns) != len(args.infiles):
        sys.stderr.write('InputError: invalid columns argument\n')
        exit()
        
    jdelim = args.delimiter if args.delimiter != None else ' '
    merge = defaultdict(str)
    counts = defaultdict(int)
    for i,tup in enumerate(zip(args.infiles, args.columns)):
        infile,col = tup
        for line in infile:
            line = line.rstrip()
            chunk = line.split(args.delimiter, col+1)[col]
            merge[chunk] += '#MERGE#'+str(i) + jdelim + line + jdelim
            counts[chunk] += 1

    for key,val in merge.iteritems():
        if not args.inner or counts[key] == len(args.infiles):
            args.outfile.write(val + '\n')
