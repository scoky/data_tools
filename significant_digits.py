#!/usr/bin/env python

import os
import sys
import argparse
import traceback
from decimal import Decimal,getcontext
from toollib.files import findNumber
from toollib.group import Group,UnsortedInputGrouper

class SDGroup(Group):
    def __init__(self, tup):
        super(SDGroup, self).__init__(tup)

    def add(self, chunks):
        val = findNumber(chunks[args.column]) + 0
        if args.append:
            args.outfile.write(args.jdelim.join(chunks) + args.jdelim)
        args.outfile.write(str(val) + '\n')

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute significant digits of column(s)')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-s', '--significant_digits', type=int, default=3)
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    args = parser.parse_args()
    args.jdelim = args.delimiter if args.delimiter != None else ' '
    getcontext().prec = args.significant_digits

    grouper = UnsortedInputGrouper(args.infile, SDGroup, [], args.delimiter)
    grouper.group()
