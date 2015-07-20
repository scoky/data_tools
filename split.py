#!/usr/bin/python

import os
import sys
import logging
import argparse
import traceback
from group import Group,UnsortedInputGrouper
from log_parsing.file_handle_dictionary import FileHandleDict

class SplitGroup(Group):
    def __init__(self, tup):
        super(SplitGroup, self).__init__(tup)
        self.filename = args.prefix+'-'.join(tup)
        self.jdelim = args.delimiter if args.delimiter != None else ' '
        args.file_dict[self.filename] = open(self.filename, 'a' if args.append else 'w')

    def add(self, chunks):
        if self.filename not in args.file_dict:
            args.file_dict[self.filename] = open(self.filename, 'a')
        args.file_dict[self.filename].write(self.jdelim.join(chunks) + '\n')

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Split a file on column(s).')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-p', '--prefix', default='split-')
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-a', '--append', default=False, action='store_true')
    args = parser.parse_args()
    args.file_dict = FileHandleDict()

    grouper = UnsortedInputGrouper(args.infile, SplitGroup, args.group, args.delimiter)
    grouper.group()
    args.file_dict.close_all()

