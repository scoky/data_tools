#!/usr/bin/env python

import os
import sys
import argparse
from collections import defaultdict
from itertools import product
from toollib.files import ParameterParser

def inner_join(args):
    tables = []
    for infile,cols in zip(args.infiles, args.on):
        args.outfile.header.addCols(infile.header.columns)
        tables.append(defaultdict(list))
        for chunks in infile:
            key = tuple([chunks[c] for c in cols])
            if len(tables) == 1 or key in tables[0]:
                tables[-1][key].append(chunks)

        for tbl in tables[:-1]:
            for key in tbl.keys():
                if key not in tables[-1]:
                    del tbl[key]
        
    for key in tables[0]:
        for rows in product(*[table[key] for table in tables]):
            chunks = []
            for row in rows:
                chunks.extend(row)
            args.outfile.write(chunks)

def left_outer_join(args):
    tables = []
    for infile,cols in zip(args.infiles, args.on):
        args.outfile.header.addCols(infile.header.columns)
        width = len(infile.header.columns)
        tables.append(defaultdict(list))
        for chunks in infile:
            width = max(len(chunks), width)
            key = tuple([chunks[c] for c in cols])
            if len(tables) == 1 or key in tables[0]:
                tables[-1][key].append(chunks)

        if len(tables) > 1:
            for key in tables[0]:
                if key not in tables[-1]:
                    tables[-1][key].append([None] * width)
        
    for key in tables[0]:
        for rows in product(*[table[key] for table in tables]):
            chunks = []
            for row in rows:
                chunks.extend(row)
            args.outfile.write(chunks)

def outer_join(args):
    tables = []
    widths = []
    for infile,cols in zip(args.infiles, args.on):
        args.outfile.header.addCols(infile.header.columns)
        width = len(infile.header.columns)
        tables.append(defaultdict(list))
        for chunks in infile:
            width = max(len(chunks), width)
            key = tuple([chunks[c] for c in cols])
            tables[-1][key].append(chunks)
            if key not in tables[0]:
                for tbl,w in zip(tables[:-1], widths):
                    tbl[key].append([None] * w)

        widths.append(width)
        for key in tables[0]:
            if key not in tables[-1]:
                tables[-1][key].append([None] * width)
        
    for key in tables[0]:
        for rows in product(*[table[key] for table in tables]):
            chunks = []
            for row in rows:
                chunks.extend(row)
            args.outfile.write(chunks)

if __name__ == "__main__":
    pp = ParameterParser('Join files on column(s)', columns = 0, infiles = '*', group = False, append = False)
    pp.parser.add_argument('-m', '--method', choices = ['inner', 'left_outer', 'outer'], default='inner')
    pp.parser.add_argument('-o', '--on', nargs='+', default=['0'], help='columns to join upon')
    args = pp.parseArgs()
    args = pp.getArgs(args)
    if len(args.on) == 1:
        args.on = args.on*len(args.infiles)
    if len(args.on) != len(args.infiles):
        raise Exception('InputError: invalid columns argument\n')
    cols = []
    for infile,c in zip(args.infiles, args.on):
        cols.append(infile.header.indexes(c.split('+')))
    args.on = cols
    
    if args.method == 'inner':
        inner_join(args)
    elif args.method == 'left_outer':
        left_outer_join(args)
    else:
        outer_join(args)

