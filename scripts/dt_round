#!/usr/bin/env python

import os
import sys
import math
from decimal import Decimal,getcontext,ROUND_FLOOR
from data_tools.files import findNumber,ParameterParser
from data_tools.group import Group,run_grouping

class RoundGroup(Group):
    def __init__(self, tup):
        super(RoundGroup, self).__init__(tup)

    def add(self, chunks):
        for c in args.columns:
            chunks[c] = args.quantF(args.binF(findNumber(chunks[c]))) + zero
        args.outfile.write(chunks)

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
    pp = ParameterParser('Compute pdf', columns = '*', labels = [None], group = False, ordered = False, append = False)
    pp.parser.add_argument('-q', '--quantize', type=Decimal, default=None, help='fixed exponent (e.g., 10, 1, 0.1)')
    pp.parser.add_argument('-s', '--significantDigits', type=int, default=None, help='number of significant digits')
    pp.parser.add_argument('-b', '--bin', type=Decimal, default=None, help='fit into bins, applies the formula: f(x) = floor(x / b) * b')
    args = pp.parseArgs()
    args.labels = []
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
