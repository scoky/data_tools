#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.lib.files import FileWriter,ParameterParser,openFile
from data_tools.lib.group import Group,run_grouping
from data_tools.lib.file_handle_dictionary import FileHandleDict

class SplitGroup(Group):
    def __init__(self, tup):
        super(SplitGroup, self).__init__(tup)
        if args.fuzz:
            tup = str(args.fuzz(tup))
        else:
            tup = '_'.join(tup)
        self.filename = args.prefix+tup
        self.delimiter = args.infile.delimiter if args.infile.delimiter else ' '

        if not args.append and self.filename not in args.files:
            args.file_dict[self.filename] = openFile(self.filename, 'w')
            if args.infile.hasHeader:
                args.file_dict[self.filename].write(self.delimiter.join(map(str, args.infile.header.columns))+'\n')
        args.files.add(self.filename)

    def add(self, chunks):
        if self.filename not in args.file_dict:
            args.file_dict[self.filename] = openFile(self.filename, 'a')
        args.file_dict[self.filename].write(self.delimiter.join(chunks) + '\n')

    def done(self):
        pass

if __name__ == "__main__":
    pp = ParameterParser('Split a file on column(s)', columns = 0)
    pp.parser.add_argument('-p', '--prefix', default='split-')
    pp.parser.add_argument('-f', '--fuzz', default=None, help='lambda specifying fuzz for group assignments')
    args = pp.parseArgs()
    args = pp.getArgs(args)
    args.file_dict = FileHandleDict()
    if args.fuzz:
        args.fuzz = eval(args.fuzz)

    args.files = set()
    run_grouping(args.infile, SplitGroup, args.group, args.ordered)
    args.file_dict.close_all()

