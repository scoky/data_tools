#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper
from decimal import Decimal
from numpy import convolve as np_convolve

class ConvolveGroup(Group):
    def __init__(self, tup):
        super(ConvolveGroup, self).__init__(tup)
        self.vals = []

    def add(self, chunks):
        self.vals.append(findNumber(chunks[args.column]))

    def done(self):
        if len(self.tup) > 0:
            prefix = args.jdelim.join(self.tup) + args.jdelim
        else:
            prefix = ''
            
        for v in np_convolve(args.function, self.vals, mode=args.mode):
            args.outfile.write(prefix + str(v) + '\n')

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute maximum of column(s)')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-m', '--mode', default='full', choices=['full', 'same', 'valid'])
    parser.add_argument('-f', '--function', default=[Decimal('0.333'), Decimal('0.334'), Decimal('0.333')], type=Decimal, nargs='+', help='append result to columns')
    args = parser.parse_args()
    args.jdelim = args.delimiter if args.delimiter != None else ' '
    
    grouper = UnsortedInputGrouper(args.infile, ConvolveGroup, args.group, args.delimiter)
    grouper.group()
