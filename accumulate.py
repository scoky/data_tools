#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping

class AccumulateGroup(Group):
    def __init__(self, tup):
        super(AccumulateGroup, self).__init__(tup)
        self.total = [0]*len(args.columns)
        if not args.append and len(self.tup) > 0:
            self.prefix = args.jdelim.join(self.tup) + args.jdelim
        else:
            self.prefix = ''

    def add(self, chunks):
        self.total[:] = [t+findNumber(chunks[c]) for t,c in zip(self.total,args.columns)]
        if args.append:
            self.prefix = args.jdelim.join(chunks) + args.jdelim
        args.outfile.write(self.prefix + args.jdelim.join(map(str,self.total)) + '\n')

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Accumulate the values of a column(s)')
    parser.add_argument('infile', nargs='?', type=FileReader, default=FileReader(sys.stdin))
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default=[0])
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-a', '--append', action='store_true', default=False)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    if args.append:
        args.outheader = args.inheader.copy()
    else:
        args.outheader = Header()
        args.outheader.addCols(args.inheader.names(args.group))
    args.outheader.addCols(col+'_accumulate' for col in args.inheader.names(args.columns))
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.columns = args.inheader.indexes(args.columns)
    args.group = args.inheader.indexes(args.group)
        
    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, AccumulateGroup, args.group, args.delimiter, args.ordered)

