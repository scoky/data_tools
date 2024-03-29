#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.files import ParameterParser
from collections import defaultdict

def difference_append(args):
    data = defaultdict(list)
    first = True
    for infile,cols in zip(args.infiles, args.on):
        for chunks in infile:
            key = tuple([chunks[col] for col in cols])
            if first:
                data[key].append(chunks)
            elif key in data:
                del data[key][-1]
                if len(data[key]) == 0:
                    del data[key]
        first = False
    return data

def difference(args):
    data = defaultdict(int)
    first = True
    for infile,cols in zip(args.infiles, args.on):
        for chunks in infile:
            key = tuple([chunks[col] for col in cols])
            if first:
                data[key] += 1
            elif key in data:
                data[key] -= 1
                if data[key] == 0:
                    del data[key]
        first = False
    return data

if __name__ == "__main__":
    pp = ParameterParser('Compute difference of column(s)', columns = 0, infiles = '*', group = False, ordered = False)
    pp.parser.add_argument('-o', '--on', nargs='+', default=['0'])
    args = pp.parseArgs()
    if len(args.on) == 1:
        args.on = args.on * len(args.infiles)
    if len(args.on) != len(args.infiles):
        sys.exit('InputError: invalid columns argument')
    cols = []
    for infile,c in zip(args.infiles, args.on):
        cols.append(infile.header.indexes(c.split('+')))
    args.on = cols
    args = pp.getArgs(args)
    if args.infiles[0].hasHeader:
        if args.append:
            args.outfile.header.addCols(args.infiles[0].header.columns)
        else:
            args.outfile.header.addCols(args.infiles[0].header.names(args.on[0]))


    if args.append:
        data = difference_append(args)
    else:
        data = difference(args)
        
    for key,val in data.items():
        if args.append:
            for v in val:
                args.outfile.write(v)
        else:
            for i in range(val):
                args.outfile.write(key)

