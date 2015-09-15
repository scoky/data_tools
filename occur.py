#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper
from decimal import Decimal

class OccurGroup(Group):
    def __init__(self, tup):
        super(OccurGroup, self).__init__(tup)
        if 'first' in args.order:
            self.add = self.addFirst
        else:
            self.add = self.addNothing
        self.last = None

    def addFirst(self, chunks):
        args.outfile.write(args.jdelim.join(chunks) + '\n')
        self.add = self.addNothing
        
    def addNothing(self, chunks):
        self.last = chunks

    def done(self):
        if self.last is not None and 'last' in args.order:
            args.outfile.write(args.jdelim.join(self.last) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Output the first/last occurance of a group')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--order', nargs='+', default=['first'], choices=['first', 'last'])
    args = parser.parse_args()

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    grouper = UnsortedInputGrouper(args.infile, OccurGroup, args.group, args.delimiter)
    grouper.group()
