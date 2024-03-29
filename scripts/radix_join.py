#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.files import FileReader,ParameterParser

if __name__ == "__main__":
    # set up command line args
    pp = ParameterParser('Join data on radix tree', columns = 1, group = False, append = False)
    pp.parser.add_argument('-p', '--prefix_file', help='file containing list of cidrs')
    pp.parser.add_argument('-i', '--prefix_index', default=0, help='field containing the cidr')
    pp.parser.add_argument('-j', '--join_method', choices=['inner', 'left_outer', 'outer'], default='inner', help='determines whether ips that do not match any cidr are dropped')
    args = pp.parseArgs()
    args = pp.getArgs(args)
    args.prefix_file = FileReader(args.prefix_file, args)
    args.prefix_index = args.prefix_file.header.index(args.prefix_index)

    args.outfile.header.addCols(args.infile.header.columns)
    args.outfile.header.addCols(args.prefix_file.header.columns)
    import radix
    r = radix.Radix()
    columns = 0
    for line in args.prefix_file:
        n = r.add(line[args.prefix_index])
        n.data['line'] = line
        n.data['count'] = 0
        columns = max(columns, len(line))

    empty = [None] * columns
    columns = 0
    for line in args.infile:
        columns = max(columns, len(line))
        m = r.search_best(line[args.column])
        if m is None and args.join_method != 'inner':
            args.outfile.write(line + empty)
        elif m is not None:
            args.outfile.write(line + m.data['line'])
            m.data['count'] += 1
    if args.join_method == 'outer':
        empty = [None] * columns
        for m in r:
            if m.data['count'] == 0:
                args.outfile.write(empty + m.data['line'])
