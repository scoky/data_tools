#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.files import findNumber,ParameterParser
from data_tools.group import Group,run_grouping
from decimal import Decimal
from numpy import convolve as np_convolve

class ConvolveGroup(Group):
    def __init__(self, tup):
        super(ConvolveGroup, self).__init__(tup)
        self.vals = []
        self.add = self._addall if args.append else self._add

    def _add(self, chunks):
        self.vals.append(findNumber(chunks[args.column]))
    def _addall(self, chunks):
        self.vals.append(chunks)

    def done(self):
        if args.append:
            for i,v in enumerate(np_convolve(args.function, [findNumber(val[args.column]) for val in self.vals], mode=args.mode)):
#                if args.mode == 
                args.outfile.write(self.vals[i] + [v])
        else:
            for v in np_convolve(args.function, self.vals, mode=args.mode):
                args.outfile.write(self.tup + [v])

if __name__ == "__main__":
    pp = ParameterParser('Convolve on a column', columns = 1, labels = [None], append = False)
    pp.parser.add_argument('-m', '--mode', default='full', choices=['full', 'same', 'valid'])
    pp.parser.add_argument('-f', '--function', default=[Decimal('0.333'), Decimal('0.334'), Decimal('0.333')], type=Decimal, nargs='+', help='append result to columns')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_convolve']
    args = pp.getArgs(args)
    args.append = False

    run_grouping(args.infile, ConvolveGroup, args.group, args.ordered)

