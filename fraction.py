#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper

class FractionGroup(Group):
    def __init__(self, tup):
        super(FractionGroup, self).__init__(tup)
        self.rows = []

    def add(self, chunks):
        self.rows.append(chunks)

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        total = sum( (findNumber(r[args.column]) for r in self.rows) )
        for r in self.rows:
            args.outfile.write(jdelim.join(r) + jdelim + str(findNumber(r[args.column]) / total) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute fraction from column(s)')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()

    grouper = UnsortedInputGrouper(args.infile, FractionGroup, args.group, args.delimiter)
    grouper.group()
