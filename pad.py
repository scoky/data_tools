#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper

class PadGroup(Group):
    def __init__(self, tup):
        super(PadGroup, self).__init__(tup)
        self.present = set()

    def add(self, chunks):
        self.present.add(chunks[args.column])
        args.outfile.write(args.jdelim.join(chunks) + '\n')

    def done(self):
        for element in args.elements:
            if element not in self.present:
                args.outfile.write((args.pad + '\n') % (self.tup, element))
                

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Generate additional rows to pad input')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-l', '--listfile', help='File containing list elements, one per line.')
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-p', '--pad', default='%s %s 0')
    args = parser.parse_args()
    
    args.jdelim = args.delimiter if args.delimiter else ' '
    args.elements = set()
    with open(args.listfile, 'r') as f:
        for line in f:
            args.elements.add(line.rstrip())

    grouper = UnsortedInputGrouper(args.infile, PadGroup, args.group, args.delimiter)
    grouper.group()
