#!/usr/bin/python

import os
import sys
import argparse
from input_handling import FileReader,Header

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute union of column(s)')
    parser.add_argument('infiles', nargs='+', default=[sys.stdin])
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default=[0])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    if len(args.columns) == 1:
        args.columns = args.columns*len(args.infiles)
    if len(args.columns) != len(args.infiles):
        sys.stderr.write('InputError: invalid columns argument\n')
        exit()

    # Handle headers
    args.infiles = [FileReader(infile) for infile in args.infiles]
    names = [infile.Header().name(col) for infile,col in zip(args.infiles, args.columns)]
    args.columns = [infile.Header().index(col) for infile,col in zip(args.infiles, args.columns)]
    name = "_".join(names) + "_union"
    outheader = Header()
    outheader.addCol(name)
    args.outfile.write(outheader.value())
    
    res = set()
    for infile,col in zip(args.infiles, args.columns):
        for line in infile:
            chunk = line.rstrip().split(args.delimiter)[col]
            if chunk not in res:
                res.add(chunk)
                args.outfile.write(chunk + '\n')
        infile.close()

