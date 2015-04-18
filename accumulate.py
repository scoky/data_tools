#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper

class AccumulateGroup(Group):
    def __init__(self, tup):
        super(AccumulateGroup, self).__init__(tup)
        self.total = 0
        self.jdelim = args.delimiter if args.delimiter != None else ' '

    def add(self, chunks):
        val = findNumber(chunks[args.column])
        self.total += val
        if args.append:
            args.outfile.write(self.jdelim.join(chunks) + self.jdelim)
        else:
            if len(self.tup) > 0:
                args.outfile.write(self.jdelim.join(self.tup) + self.jdelim)
        args.outfile.write(str(self.total) + '\n')

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Accumulate the values of a column')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-a', '--append', action='store_true', default=False)
    args = parser.parse_args()

    grouper = UnsortedInputGrouper(args.infile, AccumulateGroup, args.group, args.delimiter)
    grouper.group()
