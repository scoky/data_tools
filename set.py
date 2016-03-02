#!/usr/bin/python

import os
import sys
import argparse
from input_handling import FileReader,Header
from group import Group,run_grouping

class SetGroup(Group):
    def __init__(self, tup):
        super(SetGroup, self).__init__(tup)

    def add(self, chunks):
        if args.append:
            args.outfile.write(args.jdelim.join(chunks) + '\n')
        else:
            args.outfile.write(args.jdelim.join(self.tup) + '\n')
        self.add = self.noop
                
    def noop(self, chunks):
        pass

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute the set of strings from a column in files. Maintains first appearance order.')
    parser.add_argument('infile', nargs='?', type=FileReader, default=FileReader(sys.stdin))
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default=[0])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-a', '--append', action='store_true', default=False)
    args = parser.parse_args()

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    if args.append:
        args.outheader = args.inheader.copy()
    else:
        args.outheader = Header()
        args.outheader.addCols(args.inheader.names(args.columns))
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.columns = args.inheader.indexes(args.columns)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, SetGroup, args.columns, args.delimiter, False)

