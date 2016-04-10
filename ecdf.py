#!/usr/bin/env python

import os
import sys
import argparse
import operator
from decimal import Decimal,getcontext
from toollib.files import findNumber,ParameterParser
from collections import defaultdict

def ecdfFile(infile, outfile, column=0, quant=None, sigDigits=None, binColumn=None, padding=[]):
    if len(padding) % 2 != 0:
        raise Exception('Invalid padding!')

    # Set precision
    if sigDigits:
        prevSigDigits = getcontext().prec
        getcontext().prec = sigDigits

    # Quantize input
    if quant:
        getFunc = getQuantNumber
    else:
        getFunc = getNumber

    # Input is binned
    if not binColumn is None:
        addFunc = getBinNumber
    else:
        addFunc = getOneNumber

    bins = defaultdict(int)
    total = 0

    for chunks in infile:
        value = getFunc(chunks, column, quant)
        count = addFunc(chunks, binColumn)
        bins[value] += count
        total += count

    # Return to the default significant digits
    if sigDigits:
        getcontext().prec = prevSigDigits

    # Insert padding
    i = 0
    while i+1 < len(padding):
        bins[padding[i]+zero] += padding[i+1]
        total += padding[i+1]
        i += 2

    accum = 0
    keys = sorted(bins)
    if len(keys) > 0:
        outfile.write([keys[0], 0])
    for key in keys:
        accum += bins[key]
        outfile.write([key, Decimal(accum) / total])
        
zero = Decimal(0)
def getQuantNumber(vals, col, quant):
    return findNumber(vals[col]).quantize(quant) + zero
def getNumber(vals, col, quant):
    return findNumber(vals[col]) + zero

def getBinNumber(vals, col):
    return int(vals[col])
def getOneNumber(vals, col):
    return 1

if __name__ == "__main__":
    pp = ParameterParser('Compute pdf', columns = 1, labels = [None], append = False, group = False)
    pp.parser.add_argument('-b', '--bin', default=None, help='column containing bin counts')
    pp.parser.add_argument('-q', '--quantize', type=Decimal, default=None, help='fixed exponent')
    pp.parser.add_argument('-s', '--significantDigits', type=int, default=None, help='number of significant digits')
    pp.parser.add_argument('-p', '--padding', nargs='+', type=Decimal, default=[], help='additional binned values to add. format: "value count"')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = ['x', 'y']
    args = pp.getArgs(args)
    args.bin = args.infile.header.index(args.bin)

    ecdfFile(args.infile, args.outfile, column=args.column, quant=args.quantize, sigDigits=args.significantDigits,\
       binColumn=args.bin, padding=args.padding)


