#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper

class NumberLinesGroup(Group):
    def __init__(self, tup):
        super(NumberLinesGroup, self).__init__(tup)
        self.count = args.initial
        self.jdelim = args.delimiter if args.delimiter != None else ' '

    def add(self, chunks):
        args.outfile.write(self.jdelim.join(chunks) + self.jdelim + str(self.count) + '\n')
        self.count += 1

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Number lines in file')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-i', '--initial', type=int, default=1)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()

    grouper = UnsortedInputGrouper(args.infile, NumberLinesGroup, args.group, args.delimiter)
    grouper.group()
