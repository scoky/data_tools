#!/usr/bin/python

import os
import sys
import argparse
from collections import defaultdict
from decimal import Decimal
from input_handling import findNumber,FileReader,Header
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
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', default=0)
    parser.add_argument('-b', '--bin', default=None)
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
    args.outheader.addCol(args.inheader.name(args.column)+'_mode')
    args.outheader.addCol(args.inheader.name(args.column)+'_mode_count')
    args.outheader.addCol(args.inheader.name(args.column)+'_count')
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.column = args.inheader.index(args.column)
    args.group = args.inheader.indexes(args.group)
    args.bin = args.inheader.index(args.bin)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, ModeGroup, args.group, args.delimiter, args.ordered)

