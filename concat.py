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
    while len(args.infiles) > 0:
        lines = [infile.readline().rstrip() for infile in args.infiles]
        out = []
        for i,line in enumerate(lines):
            if line:
                out.append(line)
            else:
                del args.infiles[i]
        if len(out) > 0:
            args.outfile.write(jdelim.join(out) + '\n')
