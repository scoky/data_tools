#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,FileReader,Header,openFile
from group import Group,run_grouping
from log_parsing.file_handle_dictionary import FileHandleDict

class SplitGroup(Group):
    def __init__(self, tup):
        super(SplitGroup, self).__init__(tup)
        if args.fuzz:
            tup = str(args.fuzz(tup))
        else:
            tup = '_'.join(tup)
        self.filename = args.prefix+tup

        if not args.append and self.filename not in args.files:
            args.file_dict[self.filename] = openFile(self.filename, 'w')
            args.file_dict[self.filename].write(args.outheader.value())
        args.files.add(self.filename)

    def add(self, chunks):
        if self.filename not in args.file_dict:
            args.file_dict[self.filename] = openFile(self.filename, 'a')
        args.file_dict[self.filename].write(args.jdelim.join(chunks) + '\n')

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Split a file on column(s).')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-p', '--prefix', default='split-')
    parser.add_argument('-g', '--group', nargs='+', default=[])
    parser.add_argument('-f', '--fuzz', default=None, help='lambda specifying fuzz for group assignments')
    parser.add_argument('-a', '--append', default=False, action='store_true')
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.file_dict = FileHandleDict()
    if args.fuzz:
        args.fuzz = eval(args.fuzz)
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    args.outheader = args.inheader.copy()
    # Get columns for use in computation
    args.group = args.inheader.indexes(args.group)

    args.files = set()
    args.jdelim = args.delimiter if args.delimiter != None else ' '
    run_grouping(args.infile, SplitGroup, args.group, args.delimiter, args.ordered)
    args.file_dict.close_all()

