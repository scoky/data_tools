#!/usr/bin/python

import os
import sys
import argparse
import traceback
from decimal import Decimal,InvalidOperation
from sklearn.cluster import DBSCAN

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Cluster input')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-f', '--first', type=int, default=0)
    parser.add_argument('-s', '--second', type=int, default=1)
    parser.add_argument('-r', '--range', type=int, default=2)
    parser.add_argument('-e', '--epsilon', type=float, default=0.5)
    parser.add_argument('-m', '--min_samples', type=int, default=5)
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()

    labelToPos = {}
    matrixDict = {}
    count = 0
    for line in args.infile:
        chunks = line.rstrip().split(args.delimiter)
        first = chunks[args.first]
        second = chunks[args.second]
        distance = float(chunks[args.range])
        if first not in labelToPos:
            labelToPos[first] = count
            count += 1
        if second not in labelToPos:
            labelToPos[second] = count
            count += 1
        matrixDict[(labelToPos[first], labelToPos[second])] = distance

    matrix = [[0]*len(count) for i in range(len(count))]
    for keys,distance in matrixDict.iteritems():
        matrix[keys[0]][keys[1]] = distance
        matrix[keys[1]][keys[0]] = distance
        
    db = DBSCAN(eps=args.epsilon, metric='precomputed', min_samples=args.min_samples)
    output = db.fit(matrix)
    
    jdelim = args.delimiter if args.delimiter != None else ' '
    for label,i in labelToPos.iteritems():
        args.outfile.write(label + jdelim + str(output.labels_[i]) + '\n')
