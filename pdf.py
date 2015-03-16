#!/usr/bin/python

import os
import sys
import logging
import argparse
import traceback
import operator
from decimal import Decimal,getcontext
from input_handling import findNumber,parseLines
from collections import defaultdict

def pdfFile(infile, outfile, column=0, quant=None, sigDigits=None, binColumn=None, delimiter=None, order='key', padding=[]):
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
    if binColumn:
        addFunc = getBinNumber
    else:
        addFunc = getOneNumber

    jdelim = delimiter if delimiter != None else ' '

    bins = defaultdict(int)
    total = 0

    for line in infile:
        chunks = line.rstrip().split(delimiter)
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

    for key in bins:
        bins[key] = Decimal(bins[key])/total

    sort_bins = sorted(bins.items(), key=operator.itemgetter(0 if order=='key' else 1))
    for pair in sort_bins:
        outfile.write(jdelim.join(map(str, pair))+'\n')
        
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
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute pdf')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0, help='column contain values')
    parser.add_argument('-b', '--bin', type=int, default=None, help='column containing bin counts')
    parser.add_argument('-q', '--quantize', type=Decimal, default=None, help='fixed exponent')
    parser.add_argument('-s', '--significantDigits', type=int, default=None, help='number of significant digits')
    parser.add_argument('-d', '--delimiter', default=None, help='delimiter between columns in file')
    parser.add_argument('-r', '--order', choices=['key', 'value'], default='key', help='sort order of the output')
    parser.add_argument('-p', '--padding', nargs='+', type=Decimal, default=[], help='additional binned values to add. format: "value count"')
    args = parser.parse_args()

    pdfFile(args.infile, args.outfile, column=args.column, quant=args.quantize, sigDigits=args.significantDigits,\
       binColumn=args.bin, delimiter=args.delimiter, order=args.order, padding=args.padding)


