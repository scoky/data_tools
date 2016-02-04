#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping
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
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', default=0)
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-m', '--mode', default='full', choices=['full', 'same', 'valid'])
    parser.add_argument('-f', '--function', default=[Decimal('0.333'), Decimal('0.334'), Decimal('0.333')], type=Decimal, nargs='+', help='append result to columns')
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    if args.append:
        args.outheader = args.inheader.copy()
    else:
        args.outheader = Header()
        args.outheader.addCols(args.inheader.names(args.group))
    args.outheader.addCol(args.inheader.name(args.column)+'_convolve')
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.column = args.inheader.index(args.column)
    args.group = args.inheader.indexes(args.group)
    
    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, ConvolveGroup, args.group, args.delimiter, args.ordered)

