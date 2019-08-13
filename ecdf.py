#!/usr/bin/env python

import os
import sys
import argparse
import operator
from decimal import Decimal,getcontext
from toollib.files import findNumber,ParameterParser
from collections import defaultdict
from toollib.group import Group,run_grouping

class EcdfGroup(Group):
    def __init__(self, tup):
        super(EcdfGroup, self).__init__(tup)
        self.bins = defaultdict(int)
        self.add = self.addVal if args.bin is None else self.addBin
        self.total = 0

    def addVal(self, chunks):
        self.bins[args.getFunc(chunks, args.column, args.quantize)] += 1
        self.total += 1

    def addBin(self, chunks):
        c = float(findNumber(chunks[args.bin]))
        self.bins[args.getFunc(chunks, args.column, args.quantize)] += c
        self.total += c

    def done(self):
        # Return to the default significant digits
        if args.significantDigits:
            getcontext().prec = args.prevSigDigits
        # Insert padding
        i = 0
        while i+1 < len(args.padding):
            # Add zero to make sure that the sig digits gets set correctly
            self.bins[args.padding[i]+zero] += args.padding[i+1]
            self.total += args.padding[i+1]
            i += 2

        accum = 0.0
        keys = sorted(self.bins)
        if len(keys) > 0:
            args.outfile.write(self.tup + [keys[0], 0])
        for key in keys:
            accum += self.bins[key]
            args.outfile.write(self.tup + [key, accum / self.total])
        if len(keys) > 0:
            args.outfile.write(self.tup + [keys[-1], 1])

zero = Decimal(0)
def getQuantNumber(vals, col, quant):
    return findNumber(vals[col]).quantize(quant) + zero
def getNumber(vals, col, quant):
    return findNumber(vals[col]) + zero

if __name__ == "__main__":
    pp = ParameterParser('Compute pdf', columns = 1, labels = [None], append = False)
    pp.parser.add_argument('-b', '--bin', default=None, help='column containing bin counts')
    pp.parser.add_argument('-q', '--quantize', type=Decimal, default=None, help='fixed exponent')
    pp.parser.add_argument('-s', '--significantDigits', type=int, default=None, help='number of significant digits')
    pp.parser.add_argument('-p', '--padding', nargs='+', type=float, default=[], help='additional binned values to add. format: "value count"')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = ['x', 'y']
    args = pp.getArgs(args)
    args.bin = args.infile.header.index(args.bin)
    if len(args.padding) % 2 != 0:
        raise Exception('Invalid padding!')

    # Set precision
    if args.significantDigits:
        args.prevSigDigits = getcontext().prec
        getcontext().prec = args.significantDigits

    # Quantize input
    if args.quantize:
        args.getFunc = getQuantNumber
    else:
        args.getFunc = getNumber

    run_grouping(args.infile, EcdfGroup, args.group, args.ordered)
