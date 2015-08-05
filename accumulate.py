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
        self.total = [0]*len(args.columns)
        self.jdelim = args.delimiter if args.delimiter != None else ' '
        if args.append:
            self.prefix = self.jdelim.join(chunks) + self.jdelim
        elif len(self.tup) > 0:
            self.prefix = self.jdelim.join(self.tup) + self.jdelim
        else:
            self.prefix = ''

    def add(self, chunks):
        self.total = [t+findNumber(chunks[c]) for t,c in zip(self.total,args.columns)]
        args.outfile.write(self.prefix + self.jdelim.join(map(str,self.total)) + '\n')

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Accumulate the values of a column')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-a', '--append', action='store_true', default=False)
    args = parser.parse_args()

    grouper = UnsortedInputGrouper(args.infile, AccumulateGroup, args.group, args.delimiter)
    grouper.group()
