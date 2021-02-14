#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.files import ParameterParser

if __name__ == "__main__":
    pp = ParameterParser('Compute union of column(s)', columns = 0, infiles = '*', group = False, append = False, ordered = False)
    pp.parser.add_argument('-o', '--on', nargs='+', default=['0'], help='columns to join upon')
    args = pp.parseArgs()
    if len(args.on) == 1:
        args.on = args.on * len(args.infiles)
    if len(args.on) != len(args.infiles):
        raise Exception('InputError: invalid columns argument\n')
    cols = []
    for infile,c in zip(args.infiles, args.on):
        cols.append(infile.header.indexes(c.split('+')))
    args.on = cols
    args = pp.getArgs(args)
    if args.infiles[0].hasHeader:
        args.outfile.header.addCols(args.infiles[0].header.names(args.on[0]))

    res = set()
    for infile,cols in zip(args.infiles, args.on):
        for chunks in infile:
            key = tuple(chunks[col] for col in cols)
            if key not in res:
                res.add(key)
                args.outfile.write(key)
        infile.close()

