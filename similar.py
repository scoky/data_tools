#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping

class SimilarGroup(Group):
    def __init__(self, tup):
        super(SimilarGroup, self).__init__(tup)
        self.bins = {}

    def add(self, chunks):
        val = chunks[args.column]
        found = False
        for k in self.bins:
            if args.similar(val, k):
                self.bins[k] += 1
                found = True
                break
        if not found:
            self.bins[val] = 1

    def done(self):
        prefix = ''
        if len(self.tup) > 0:
            prefix = args.jdelim.join(self.tup) + args.jdelim
        for k,v in self.bins.iteritems():
            args.outfile.write(prefix + k + args.jdelim + str(v) + '\n')
            
# Default handling of input value    
def nofuzz(v,u):
    return v==u

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Bin column by similarity')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', default=0)
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-s', '--similar', default=None, help='lambda specifying how to determine similarity between two arguments')
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    if not args.similar:
        args.similar = nofuzz
    else:
        args.similar = eval(args.similar)
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    args.outheader = Header()
    args.outheader.addCols(args.inheader.names(args.group))
    args.outheader.addCol(args.inheader.name(args.column))
    args.outheader.addCol(args.inheader.name(args.column) + '_count')
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.column = args.inheader.index(args.column)
    args.group = args.inheader.indexes(args.group)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, SimilarGroup, args.group, args.delimiter, args.ordered)
