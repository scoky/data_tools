#!/usr/bin/env python

import os
import sys
import argparse
from input_handling import ParameterParser

if __name__ == "__main__":
    pp = ParameterParser('Compute intersection of column(s)', columns = 0, infiles = '*', group = False, append = False, ordered = False)
    pp.parser.add_argument('-o', '--on', nargs='+', default=['0'], help='columns to join upon')
    args = pp.parseArgs()
    args = pp.getArgs(args)
    if len(args.on) == 1:
        args.on = args.on * len(args.infiles)
    if len(args.on) != len(args.infiles):
        raise Exception('InputError: invalid columns argument\n')
    cols = []
    for infile,c in zip(args.infiles, args.on):
        cols.append(infile.header.indexes(c.split('+')))
    args.on = cols

    items = None
    cur = set()
    first = True
    for infile,cols in zip(args.infiles, args.on):
        if len(args.outfile.header) == 0:
            args.outfile.header.addCols(infile.header.columns)
        for chunks in infile:
            key = tuple([chunks[col] for col in cols])
            cur.add(key)
        if first:
            items = cur
            cur = set()
        else:
            items = items & cur
            cur = set()
        first = False
        infile.close()
    
    for item in items:
        args.outfile.write(list(item))
