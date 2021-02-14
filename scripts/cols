#!/usr/bin/env python

import os
import sys
from data_tools.files import ParameterParser

if __name__ == "__main__":
    pp = ParameterParser('Select columns from a file', columns = '*', group = False, append = False, labels = [None], ordered = False)
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = args.columns_names
    args = pp.getArgs(args)

    for chunks in args.infile:
        args.outfile.write([chunks[i] for i in args.columns])

