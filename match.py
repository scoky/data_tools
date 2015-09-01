#!/usr/bin/python

import os
import sys
import argparse
import traceback
from collections import defaultdict

class match(object):
    def __init__(self):
        self.value = ''
        self.srcs = set()
        
    def add(self, i, line):
        self.srcs.add(i)
        self.value += '#MATCH#'+str(i) + args.jdelim + line + args.jdelim

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Match files on column(s)')
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
        
    args.jdelim = args.delimiter if args.delimiter != None else ' '
    merge = defaultdict(list)
    for i,tup in enumerate(zip(args.infiles, args.columns)):
        infile,col = tup
        for line in infile:
            line = line.rstrip()
            chunk = line.split(args.delimiter)[col]
            
            found = False
            for m in merge[chunk]:
                if i not in m.srcs:
                    m.add(i, line)
                    found = True
                    break
            if not found:
                m = match()
                m.add(i, line)
                merge[chunk].append(m)

    for key,merges in merge.iteritems():
        for m in merges:
            if not args.inner or len(m.srcs) == len(args.infiles):
                args.outfile.write(m.value + '\n')
