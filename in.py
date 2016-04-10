#!/usr/bin/env python

import os
import sys
import argparse
from toollib.files import ParameterParser,FileReader

def compareIn(infile, outfile, columns, elements, testIn=True):
    for chunks in infile:
        c = tuple([chunks[i] for i in columns])
        if (testIn and c in elements) or (not testIn and c not in elements):
            outfile.write(chunks)

def main():
    elements = set()
    for item in args.elements:
        elements.add(tuple(item,))
    for listfile in args.files:
        with FileReader(listfile, args) as f:
            for chunks in f:
                elements.add(tuple(chunks))

    compareIn(args.infile, args.outfile, args.columns, elements, not args.notin)

if __name__ == "__main__":
    pp = ParameterParser('Output rows where column(s) are in list', columns = '*', group = False, append = False, ordered = False)
    pp.parser.add_argument('-n', '--notin', action='store_true', default=False)
    pp.parser.add_argument('-e', '--elements', nargs='+', default=[], help='List of elements')
    pp.parser.add_argument('-f', '--files', nargs='+', default=[], help='Files containing list elements, one per line.')
    args = pp.parseArgs()
    args.append = True
    args = pp.getArgs(args)

    main()


