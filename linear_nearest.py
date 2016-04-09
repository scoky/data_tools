#!/usr/bin/env python

import os
import sys
import argparse
from collections import deque
from input_handling import ParameterParser,findNumber
from group import Group,run_grouping
from heapq import heappush, heappop
        
class KNearGroup(Group):
    def __init__(self, tup):
        super(KNearGroup, self).__init__(tup)
        self.past = deque()
        self.future = deque()

    def add(self, chunks):
        val = findNumber(chunks[args.column])
        self.future.append(val)
        
        if len(self.future) > args.k:
            current = self.future.popleft()
            nearest = [abs(x - current) for x in self.past] + [abs(x - current) for x in self.future]
            nearest = sorted(nearest)[:args.k]
            
            args.outfile.write(self.tup + [current] + nearest)

            self.past.append(current)
            while len(self.past) > args.k:
                self.past.popleft()

    def done(self):
        while len(self.future) > 0:
            current = self.future.popleft()
            nearest = [abs(x - current) for x in self.past] + [abs(x - current) for x in self.future]
            nearest = sorted(nearest)[:args.k]

            args.outfile.write(self.tup + [current] + nearest)

            self.past.append(current)
        self.past.clear()
        
if __name__ == "__main__":
    pp = ParameterParser('Compute the k-nearest values', columns = 1, labels = [None], append = False)
    pp.parser.add_argument('-k', '--k', type=int, default=1)
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name] + ['{0}_k{1}_nearest'.format(args.column_name, k+1) for k in range(args.k)]
    args = pp.getArgs(args)

    run_grouping(args.infile, KNearGroup, args.group, args.ordered)
