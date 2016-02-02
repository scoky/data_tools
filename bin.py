#!/usr/bin/python

import os
import sys
import argparse
from collections import defaultdict
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping

class BinGroup(Group):
    def __init__(self, tup):
        super(BinGroup, self).__init__(tup)
        self.key = str(args.fuzz(tup))

    def add(self, chunks):
        args.bins[self.key] += 1

    def done(self):
        pass
            
# Default handling of input value    
def nofuzz(v):
    return args.jdelim.join(v)

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute bins from column(s)')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-g', '--group', nargs='+', default=[0])
    parser.add_argument('-f', '--fuzz', default=None, help='lambda specifying how to fuzz bins')
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    if not args.fuzz:
        args.fuzz = nofuzz
    else:
        args.fuzz = eval(args.fuzz)
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    args.outheader = Header()
    args.outheader.addCols(args.inheader.names(args.group))
    args.outheader.addCol('_'.join(args.inheader.names(args.group)) + '_count')
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.group = args.inheader.indexes(args.group)

    args.bins = defaultdict(int)
    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, BinGroup, args.group, args.delimiter, args.ordered)
    
    for k,v in args.bins.iteritems():
        args.outfile.write(k + args.jdelim + str(v) + '\n')

