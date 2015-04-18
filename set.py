#!/usr/bin/python

import os
import sys
import logging
import argparse
import traceback
from group import Group,UnsortedInputGrouper

class SetGroup(Group):
    def __init__(self, tup):
        super(SetGroup, self).__init__(tup)
        self.uniques = set()
        self.jdelim = args.delimiter if args.delimiter != None else ' '

    def add(self, chunks):
        val = chunks[args.column]
        if val not in self.uniques:
            self.uniques.add(val)
            if args.append:
                args.outfile.write(self.jdelim.join(chunks) + '\n')
            else:
                if len(self.tup) > 0:
                    args.outfile.write(self.jdelim.join(self.tup) + self.jdelim)
                args.outfile.write(val + '\n')

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the set of strings from a column in files. Maintains first appearance order.')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-a', '--append', action='store_true', default=False)
    args = parser.parse_args()

    grouper = UnsortedInputGrouper(args.infile, SetGroup, args.group, args.delimiter)
    grouper.group()
