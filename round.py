#!/usr/bin/env python

import os
import sys
import math
from decimal import Decimal,getcontext,ROUND_FLOOR
from toollib.files import findNumber,ParameterParser
from toollib.group import Group,run_grouping

class RoundGroup(Group):
    def __init__(self, tup):
        super(RoundGroup, self).__init__(tup)
        self.row = []
        if args.append:
            self.add = self.addAppend

    def add(self, chunks):
        val = args.quantF(args.binF(findNumber(chunks[args.column]))) + zero
        args.outfile.write([val])

    def addAppend(self, chunks):
        val = args.quantF(args.binF(findNumber(chunks[args.column]))) + zero
        args.outfile.write(chunks + [val])

    def done(self):
        pass

zero = Decimal(0)
def noop(val):
    return val

def quantize(val):
    return val.quantize(args.quantize)

def binify(val):
    return (val / args.bin).to_integral_exact(rounding=ROUND_FLOOR) * args.bin

if __name__ == "__main__":
    pp = ParameterParser('Compute pdf', columns = 1, labels = [None], group = False, ordered = False)
    pp.parser.add_argument('-q', '--quantize', type=Decimal, default=None, help='fixed exponent (e.g., 10, 1, 0.1)')
    pp.parser.add_argument('-s', '--significantDigits', type=int, default=None, help='number of significant digits')
    pp.parser.add_argument('-b', '--bin', type=Decimal, default=None, help='fit into bins, applies the formula: f(x) = floor(x / b) * b')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_round']
    args = pp.getArgs(args)
    if args.significantDigits is not None:
        getcontext().prec = args.significantDigits
    if args.bin is not None:
        args.binF = binify
    else:
        args.binF = noop
    if args.quantize is not None:
        args.quantF = quantize
    else:
        args.quantF = noop

    run_grouping(args.infile, RoundGroup, [], False)
