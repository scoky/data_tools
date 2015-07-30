#!/usr/bin/python

import os
import sys
import argparse
import traceback
from collections import deque
from input_handling import findNumber
from group import Group,run_grouping

def dist(tx, ty):
    return abs(tx - ty)
    
class Neighbor(object):
    def __init__(self, t, line):
        self.t = t
        self.line = line
        self.count = 0
        self.label = -1

class DBSCANGroup(Group):
    def __init__(self, tup):
        super(DBSCANGroup, self).__init__(tup)
        self.neighbors = deque()

    def add(self, chunks):
        n = Neighbor(findNumber(chunks[args.column]), args.jdelim.join(chunks))

        # Update neighbor counts
        oldest = None
        for nn in self.neighbors:
            if dist(nn.t, n.t) <= args.epsilon:
                n.count += 1
                nn.count += 1
                if oldest == None:
                    oldest = nn
        # No neighbors for the new element, clear out old data
        if n.count == 0:
            self.empty()
        elif oldest.count >= args.min_samples: # Oldest is core
            if oldest.label != -1:
                label = oldest.label
            else:
                label = args.label
                args.label += 1
            for nn in self.neighbors:
                if nn.label == -1 and dist(nn.t, oldest.t) <= args.epsilon:
                    nn.label = label
        self.neighbors.append(n)
        
    def empty(self):
        for nn in self.neighbors:
            args.outfile.write(nn.line + args.jdelim + str(nn.label) + '\n')
        self.neighbors.clear()

    def done(self):
        self.empty()

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Cluster input')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-e', '--epsilon', type=float, default=0.5)
    parser.add_argument('-m', '--min_samples', type=int, default=5)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    args.label = 0
    run_grouping(args.infile, DBSCANGroup, args.group, args.delimiter, args.ordered)

