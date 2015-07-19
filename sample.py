#!/usr/bin/python

import os
import sys
import random
import argparse
import traceback
from input_handling import findNumber
from group import Group,run_grouping

class SampleGroup(Group):
    def __init__(self, tup):
        super(SampleGroup, self).__init__(tup)
        self.row = []

    def add(self, chunks):
        val = chunks[args.column]
        self.row.append(val)

    def done(self):
        jdelim = args.delimiter if args.delimiter != None else ' '
        prefix = ''
        if len(self.tup) > 0:
            prefix = jdelim.join(self.tup) + jdelim
        if args.replacement:
            for val in (random.choice(self.row) for n in range(args.number)):
                args.outfile.write(prefix + val + '\n')
        else:
            for val in random.sample(self.row, args.number):
                args.outfile.write(prefix + val + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Sample from column')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    parser.add_argument('-r', '--replacement', action='store_true', default=False, help='with replacement')
    parser.add_argument('-s', '--seed', type=int, default=12345)
    parser.add_argument('-n', '--number', type=int, default=10, help='number of samples')
    args = parser.parse_args()
    random.seed(args.seed)

    run_grouping(args.infile, SampleGroup, args.group, args.delimiter, args.ordered)
