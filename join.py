#!/usr/bin/python

import os
import sys
import argparse
import traceback
from collections import defaultdict

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Join files on column(s) to first file')
    parser.add_argument('infiles', nargs='*', type=argparse.FileType('r'), default=[sys.stdin])
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default=['0'], help='use + to specify multiple columns per file')
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-i', '--inner', action='store_true', default=False, help='inner join')
    args = parser.parse_args()
    if len(args.columns) == 1:
        args.columns = args.columns*len(args.infiles)
    if len(args.columns) != len(args.infiles):
        sys.stderr.write('InputError: invalid columns argument\n')
        exit()
    cols = []
    for c in args.columns:
        cols.append(map(int, c.split('+')))
    args.columns = cols
        
    jdelim = args.delimiter if args.delimiter != None else ' '
    merge = defaultdict(str)
    counts = defaultdict(int)
    for i,tup in enumerate(zip(args.infiles[1:], args.columns[1:])):
        infile,col = tup
        for line in infile:
            line = line.rstrip()
            chunks = line.split(args.delimiter)
            chunk = jdelim.join([chunks[c] for c in col])
            merge[chunk] += '#JOIN#'+str(i) + jdelim + line + jdelim
            counts[chunk] += 1
        infile.close()

    col = args.columns[0]
    for line in args.infiles[0]:
        line = line.rstrip()
        chunks = line.split(args.delimiter)
        chunk = jdelim.join([chunks[c] for c in col])
        if chunk in merge:
            line += jdelim + merge[chunk]
        if not args.inner or counts[chunk] == len(args.infiles) - 1:
            args.outfile.write(line + '\n')

