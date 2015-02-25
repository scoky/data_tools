#!/usr/bin/python

import os
import sys
import argparse
import traceback

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Concatenate files')
    parser.add_argument('infiles', nargs='+', type=argparse.FileType('r'), default=[sys.stdin])
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()

    jdelim = args.delimiter if args.delimiter != None else ' '
    lines = []
    for infile in args.infiles:
        for i,line in enumerate(infile):
            if len(lines) > i:
                lines[i] += jdelim + line.rstrip()
            else:
                lines.append(line.rstrip())
    for line in lines:
        args.outfile.write(line + '\n')
