#!/usr/bin/python

import os
import sys
import argparse
import traceback
from collections import deque
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping
from heapq import heappush, heappop
        
class KNearGroup(Group):
    def __init__(self, tup):
        super(KNearGroup, self).__init__(tup)
        self.past = deque()
        self.future = deque()
        if len(self.tup) > 0:
            self.prefix = args.jdelim.join(self.tup) + args.jdelim
        else:
            self.prefix = ''

    def add(self, chunks):
        val = findNumber(chunks[args.column])
        self.future.append(val)
        
        if len(self.future) > args.k:
            current = self.future.popleft()
            nearest = [abs(x - current) for x in self.past] + [abs(x - current) for x in self.future]
            nearest = sorted(nearest)[:args.k]
            
            args.outfile.write(self.prefix + str(current) + args.jdelim + args.jdelim.join(map(str, nearest)) + '\n')

            self.past.append(current)
            while len(self.past) > args.k:
                self.past.popleft()

    def done(self):
        while len(self.future) > 0:
            current = self.future.popleft()
            nearest = [abs(x - current) for x in self.past] + [abs(x - current) for x in self.future]
            nearest = sorted(nearest)[:args.k]

            args.outfile.write(self.prefix + str(current) + args.jdelim + args.jdelim.join(map(str, nearest)) + '\n')

            self.past.append(current)
        self.past.clear()
        
if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the k-nearest values')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', default=0)
    parser.add_argument('-k', '--k', type=int, default=1)
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    args.outheader = Header()
    args.outheader.addCols(args.inheader.names(args.group))
    args.outheader.addCol(args.inheader.name(args.column))
    for i in range(args.k):
        args.outheader.addCol(args.inheader.name(args.column)+('_k=%d_nearest' % (i+1)))
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.column = args.inheader.index(args.column)
    args.group = args.inheader.indexes(args.group)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, KNearGroup, args.group, args.delimiter, args.ordered)
