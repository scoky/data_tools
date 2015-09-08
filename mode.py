#!/usr/bin/python

import os
import sys
import argparse
import traceback
from collections import defaultdict
from decimal import Decimal
from input_handling import findNumber
from group import Group,run_grouping

class ModeGroup(Group):
    def __init__(self, tup):
        super(ModeGroup, self).__init__(tup)
        self.vals = defaultdict(int)
        self.add = self.addBin if args.bin else self.addVal

    def addVal(self, chunks):
        val = findNumber(chunks[args.column])
        self.vals[val] += 1

    def addBin(self, chunks):
        val = findNumber(chunks[args.column])
        b = int(chunks[args.bin])
        self.vals[val] += b

    def done(self):
        if len(self.tup) > 0:
            args.outfile.write(args.jdelim.join(self.tup) + args.jdelim)
        args.outfile.write(args.jdelim.join(map(str, mode(self.vals))) + '\n')

def mode(dic):
    count = 0
    maximum = -1
    max_k = None
    for k,v in dic.iteritems():
        if v > maximum:
            maximum = v
            max_k = k
        count += v
    return (max_k, maximum, count)

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the modes')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-b', '--bin', type=int, default=None)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, ModeGroup, args.group, args.delimiter, args.ordered)

