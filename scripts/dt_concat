#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.files import ParameterParser

def concat_rows():
    for infile in args.infiles:
        args.outfile.header.addCols(infile.header.columns)
    while len(args.infiles) > 0:
        lines = [infile.readline() for infile in args.infiles]
        out = []
        remove = []
        for i,line in enumerate(lines):
            if line:
                out.extend(line)
            else:
                remove.append(i)
        if 0 < len(remove) < len(args.infiles):
            sys.stderr.write('Warning: input files have different lengths!\n')
        for i in reversed(remove):
            del args.infiles[i]
        if len(out) > 0:
            args.outfile.write(out)

def concat_cols():
    args.outfile.header.addCols(args.infiles[0].header.columns)
    for infile in args.infiles:
        for line in infile:
            args.outfile.write(line)
        infile.close()

if __name__ == "__main__":
    pp = ParameterParser('Concatenate files', columns = 0, group = False, ordered = False, infiles = '*', append = False)
    pp.parser.add_argument('-m', '--method', default='columns', choices=['rows', 'columns'])
    args = pp.parseArgs()
    args = pp.getArgs(args)

    if args.method == 'columns':
        concat_cols()
    else:
        concat_rows()
