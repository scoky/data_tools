#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper
from decimal import Decimal

class AnonGroup(Group):
    def __init__(self, tup):
        super(AnonGroup, self).__init__(tup)
        self.reverse = {}
        self.forward = {}

    def add(self, chunks):
        for i in args.columns:
            if chunks[i] not in self.forward:
                val = abs(hash(chunks[i]))
                while val in self.reverse and self.reverse[val] != chunks[i]:
                    val = abs(val+1)
                self.reverse[val] = chunks[i]
                self.forward[chunks[i]] = str(val)

            chunks[i] = self.forward[chunks[i]]
        args.outfile.write(args.jdelim.join(chunks) + '\n')

    def done(self):
        if args.mapping:
            for pairs in self.forward.iteritems():
                args.mapping.write(args.jdelim.join(pairs) + '\n')
        
if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Replace column(s) with hashes for anonymization')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-m', '--mapping', type=argparse.FileType('w'), default=None)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    grouper = UnsortedInputGrouper(args.infile, AnonGroup, [], args.delimiter)
    grouper.group()
