#!/usr/bin/python

import os
import sys
from input_handling import ParameterParser,Header

if __name__ == "__main__":
    args = ParameterParser('Select columns from a file.', group = False, append = False)
    if args.infile.HasHeader():
        args.outheader = Header()
        if len(args.labels) > 0:
            if len(args.labels) != len(args.columns):
                raise Exception('Must specify labels for all columns!')
            else:
                args.outheader.addCols(args.labels)
        else:
            args.outheader.addCols(args.columns_names)
        args.outfile.write(args.outheader.value(args.outdelimiter))

    for chunks in args.infile:
        args.outfile.write(args.outdelimiter.join([chunks[i] for i in args.columns])+'\n')

