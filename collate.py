#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from collections import namedtuple

def getStrKey(line, col):
    return line.split(args.delimiter, col+1)[col]

def getNumKey(line, col):
    return findNumber(line.split(args.delimiter, col+1)[col])

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Collate multiple files')
    parser.add_argument('infiles', nargs='+', type=argparse.FileType('r'), default=[sys.stdin])
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-n', '--numerical', default=False, action='store_true')
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    if len(args.columns) == 1:
        args.columns = args.columns*len(args.infiles)
    if len(args.columns) != len(args.infiles):
        sys.stderr.write('InputError: invalid columns argument\n')
        exit()
    if args.numerical:
        getKey = getNumKey
    else:
        getKey = getStrKey
        
    File = namedtuple('File', 'file col line key')
    memory = []
    for col,infile in zip(args.columns, args.infiles):
        line = infile.readline()
        if line:
            memory.append(File(infile, col, line, getKey(line, col)))
        
    while len(memory) > 0:
        i,tup = min(enumerate(memory), key = lambda item: item[1].key)
        args.outfile.write(tup.line)
        line = tup.file.readline()
        if line:
            tup = File(tup.file, tup.col, line, getKey(line, tup.col))
            memory[i] = tup
        else:
            del memory[i]
