#!/usr/bin/python

import os
import sys
import argparse
from sklearn.cluster import DBSCAN
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping

def scan_matrix():
    labelToPos = {}
    matrixDict = {}
    count = 0
    for line in args.infile:
        chunks = line.rstrip().split(args.delimiter)
        first = chunks[args.first]
        second = chunks[args.second]
        distance = float(findNumber(chunks[args.range]))
        if first not in labelToPos:
            labelToPos[first] = count
            count += 1
        if second not in labelToPos:
            labelToPos[second] = count
            count += 1
        matrixDict[(labelToPos[first], labelToPos[second])] = distance

    matrix = [[0]*count for i in range(count)]
    for keys,distance in matrixDict.iteritems():
        matrix[keys[0]][keys[1]] = distance
        matrix[keys[1]][keys[0]] = distance
        
    db = DBSCAN(eps=args.epsilon, metric='precomputed', min_samples=args.min_samples)
    output = db.fit(matrix)
    
    for label,i in labelToPos.iteritems():
        args.outfile.write(label + args.jdelim + str(output.labels_[i]) + '\n')

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
        n = Neighbor(float(findNumber(chunks[args.range])), args.jdelim.join(chunks))

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
                                     description='Cluster input using the DBSCAN algorithm')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-f', '--first', default=0, help='first key column')
    parser.add_argument('-s', '--second', default=1, help='second key column')
    parser.add_argument('-r', '--range', default=2, help='distance between first and second keys')
    parser.add_argument('-l', '--online', action='store_true', default=False, help='changes meaning of range parameter to a monotonically increasing position value')
    parser.add_argument('-e', '--epsilon', type=float, default=0.5)
    parser.add_argument('-m', '--min_samples', type=int, default=5)
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    if args.online:
        args.outheader = args.inheader.copy()
        args.group = args.inheader.indexes(args.group)
    else:
        args.outheader = Header()
        args.outheader.addCol(args.inheader.name(args.first))
        args.first = args.inheader.index(args.first)
        args.second = args.inheader.index(args.second)
    args.outheader.addCol('cluster')
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.range = args.inheader.index(args.range)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    if args.online:
        args.label = 0
        run_grouping(args.infile, DBSCANGroup, args.group, args.delimiter, args.ordered)
    else:
        scan_matrix()

