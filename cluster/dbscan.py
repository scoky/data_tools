#!/usr/bin/env python

import os
import sys
import argparse
from sklearn.cluster import DBSCAN
sys.path.insert(1, os.path.join(os.path.dirname(__file__), os.pardir))
from toollib.files import findNumber,ParameterParser
from toollib.group import Group,run_grouping

class OfflineDBSCANGroup(Group):
    def __init__(self, tup):
        super(OfflineDBSCANGroup, self).__init__(tup)
        self.labelToPos = {}
        self.matrixDict = {}
        self.count = 0

    def add(self, chunks):
        first = chunks[args.first]
        second = chunks[args.second]
        distance = float(findNumber(chunks[args.range]))
        if first not in self.labelToPos:
            self.labelToPos[first] = self.count
            self.count += 1
        if second not in self.labelToPos:
            self.labelToPos[second] = self.count
            self.count += 1
        self.matrixDict[(self.labelToPos[first], self.labelToPos[second])] = distance

    def done(self):
        matrix = [[0]*self.count for i in range(self.count)]
        for keys,distance in self.matrixDict.iteritems():
            matrix[keys[0]][keys[1]] = distance
            matrix[keys[1]][keys[0]] = distance

        db = DBSCAN(eps=args.epsilon, metric='precomputed', min_samples=args.min_samples)
        output = db.fit(matrix)

        for label,i in self.labelToPos.iteritems():
            args.outfile.write(self.tup + [label, output.labels_[i]])

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

class OnlineDBSCANGroup(Group):
    def __init__(self, tup):
        super(OnlineDBSCANGroup, self).__init__(tup)
        self.head = self.tail = None

    def add(self, chunks):
        n = Neighbor(float(findNumber(chunks[args.range])), chunks)

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
            args.outfile.write(nn.line + [nn.label])
        self.head = self.tail = None

    def done(self):
        self.empty()

if __name__ == "__main__":
    pp = ParameterParser('Cluster input using the DBSCAN algorithm', columns = 0, labels = [None], append = False)
    pp.parser.add_argument('--online', action='store_true', default=False, help='changes meaning of range parameter to a monotonically increasing position value')
    pp.parser.add_argument('-f', '--first', default='0', help='first key column')
    pp.parser.add_argument('-s', '--second', default='1', help='second key column (offline only)')
    pp.parser.add_argument('-r', '--range', default='2', help='column with distance')
    pp.parser.add_argument('-e', '--epsilon', type=float, default=0.5)
    pp.parser.add_argument('-m', '--min_samples', type=int, default=5)
    args = pp.parseArgs()
    if args.online:
        args.append = True
    if not any(args.labels):
        if args.online:
            args.labels = ['label']
        else:
            args.labels = [args.infile.header.name(args.first), 'label']
    args = pp.getArgs(args)
    args.first = args.infile.header.index(args.first)
    args.second = args.infile.header.index(args.second)
    args.range = args.infile.header.index(args.range)

    if args.online:
        args.label = 0
        run_grouping(args.infile, OnlineDBSCANGroup, args.group, args.ordered)
    else:
        run_grouping(args.infile, OfflineDBSCANGroup, args.group, args.ordered)

