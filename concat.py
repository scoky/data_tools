#!/usr/bin/python

import os
import sys
import argparse
from input_handling import FileReader,Header

def concat_rows():
    # Write combined header
    outheader = Header()
    for inheader in args.inheaders:
        outheader.addCols(inheader)
    args.outfile.write(outheader.value())

    while len(args.infiles) > 0:
        lines = [infile.readline().rstrip() for infile in args.infiles]
        out = []
        remove = []
        for i,line in enumerate(lines):
            if line:
                out.append(line)
            else:
                remove.append(i)
        if 0 < len(remove) < len(args.infiles):
            sys.stderr.write('Warning: input files have different lengths!\n')
        for i in reversed(remove):
            del args.infiles[i]
        if len(out) > 0:
            args.outfile.write(args.jdelim.join(out) + '\n')

def concat_cols():
    # Write first header
    header = Header()
    for inheader in args.inheaders:
        if inheader and len(inheader) > 0:
            header = inheader
            break
    args.outfile.write(header.value())

    for infile in args.infiles:
        for line in infile:
            args.outfile.write(line)
        infile.close()

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Concatenate files')
    parser.add_argument('infiles', nargs='+', default=[sys.stdin])
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-m', '--method', default='columns', choices=['rows', 'columns'])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    args.infiles = [FileReader(infile) for infile in args.infiles]
    args.inheaders = [infile.Header() for infile in args.infiles]
    if args.method == 'columns':
        concat_cols()
    else:
        concat_rows()
