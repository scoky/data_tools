#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from decimal import Decimal
from group import Group,run_grouping

def dist(tx, ty):
    return abs(tx - ty)
    
class Neighbor(object):
    def __init__(self, t, line):
        self.t = t
        self.line = line
        self.count = 0
        self.label = -1
        self.next = self.prev = None

    @classmethod    
    def iterate_forward(cls, head):
        i = head
        while i != None:
            yield i
            i = i.next

    @classmethod    
    def iterate_reverse(cls, tail):
        i = tail
        while i != None:
            yield i
            i = i.prev
            
    def neighbors(self):
        i = self.prev
        while i != None and dist(i.t, self.t) <= args.epsilon:
            yield i
            i = i.prev
        i = self.next
        while i != None and dist(i.t, self.t) <= args.epsilon:
            yield i
            i = i.next

class DBSCANGroup(Group):
    def __init__(self, tup):
        super(DBSCANGroup, self).__init__(tup)
        self.head = self.tail = None

    def add(self, chunks):
        n = Neighbor(findNumber(chunks[args.column]), args.jdelim.join(chunks))

        # Update neighbor counts
        oldest = None
        for nn in Neighbor.iterate_reverse(self.tail):
            if dist(nn.t, n.t) <= args.epsilon:
                n.count += 1
                nn.count += 1
                oldest = nn
            else:
                break

        # No neighbors for the new element, clear out old data
        if n.count == 0:
            self.empty()
        elif oldest.count >= args.min_samples: # Oldest is core
            if oldest.label != -1:
                label = oldest.label
            else:
                oldest.label = label = args.label
                args.label += 1

            n.label = label
            for nn in oldest.neighbors():
                if nn.label == -1:
                    nn.label = label

        # Append onto the end of the list
        if self.tail:
            self.tail.next = n
        else:
            self.head = n
        n.prev = self.tail
        self.tail = n
        
    def empty(self):
        for nn in Neighbor.iterate_forward(self.head):
            args.outfile.write(nn.line + args.jdelim + str(nn.label) + '\n')
        self.head = self.tail = None

    def done(self):
        self.empty()

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Cluster input')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-e', '--epsilon', type=Decimal, default=Decimal('0.5'))
    parser.add_argument('-m', '--min_samples', type=int, default=5)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    args.label = 0
    run_grouping(args.infile, DBSCANGroup, args.group, args.delimiter, args.ordered)

