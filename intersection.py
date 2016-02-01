#!/usr/bin/python

import os
import sys
import argparse
from input_handling import FileReader,Header

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute intersection of column(s)')
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
        
    allitems = []
    res = set()
    cur = set()
    first = True
    name = ''
    for infile,col in zip(args.infiles, args.columns):
        infile = FileReader(infile)
        name += infile.Header().name(col)+'_'
        col = infile.Header().index(col)
        for line in infile:
            chunk = line.rstrip().split(args.delimiter)[col]
            allitems.append(chunk)
            if first:
                res.add(chunk)
                cur.add(chunk)
            else:
                cur.add(chunk)
        res = res & cur
        first = False
        cur.clear()
        infile.close()
    
    outheader = Header()
    outheader.addCol(name+'intersect')
    args.outfile.write(outheader.value())
    for item in allitems:
        if item in res:
            args.outfile.write(item + '\n')
            res.remove(item)
