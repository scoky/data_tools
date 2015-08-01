#!/usr/bin/python

import os
import sys
import argparse
import traceback
from collections import deque
from input_handling import findNumber
from group import Group,run_grouping
from heapq import heappush, heappop
        
class KNearGroup(Group):
    def __init__(self, tup):
        super(KNearGroup, self).__init__(tup)
        self.past = deque()
        self.future = deque()
        if len(self.tup) > 0:
            args.prefix = jdelim.join(self.tup) + jdelim
        else:
            args.prefix = ''

    def add(self, chunks):
        val = findNumber(chunks[args.column])
        self.future.append(val)
        
        if len(self.future) > args.k_nearest:
            current = self.future.popleft()
            nearest = [abs(x - current) for x in self.past] + [abs(x - current) for x in self.future]
            nearest = sorted(nearest)[:args.k_nearest]
            
            args.outfile.write(prefix + str(current) + args.jdelim + args.jdelim.join(nearest) + '\n')

            self.past.append(current)

    def done(self):
        while len(self.future) > 0:
            current = self.future.popleft()
            nearest = [abs(x - current) for x in self.past] + [abs(x - current) for x in self.future]
            nearest = sorted(nearest)[:args.k_nearest]

            args.outfile.write(prefix + str(current) + args.jdelim + args.jdelim.join(nearest) + '\n')

            self.past.append(current)
        
if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute minimum of column(s)')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-k', '--k_nearest', type=int, default=1)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, KNearGroup, args.group, args.delimiter, args.ordered)
