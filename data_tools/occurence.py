#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.lib.files import ParameterParser
from data_tools.lib.group import Group,run_grouping

class OccurGroup(Group):
    def __init__(self, tup):
        super(OccurGroup, self).__init__(tup)
        if 'first' in args.order:
            self.add = self.addFirst
        else:
            self.add = self.addNothing
        self.last = None

    def addFirst(self, chunks):
        args.outfile.write(chunks)
        if args.duplicate:
            self.last = chunks
        self.add = self.addNothing
        
    def addNothing(self, chunks):
        self.last = chunks

    def done(self):
        if self.last is not None and 'last' in args.order:
            args.outfile.write(self.last)

if __name__ == "__main__":
    pp = ParameterParser('Output the first/last occurance of a group', columns = False, append = False, ordered = True)
    pp.parser.add_argument('-o', '--order', nargs='+', default=['first'], choices=['first', 'last'])
    pp.parser.add_argument('-d', '--duplicate', action='store_true', default=False, help='if order is first and last and there is only 1 group member, print same line twice')
    args = pp.parseArgs()
    args.append = True
    args = pp.getArgs(args)

    run_grouping(args.infile, OccurGroup, args.group, args.ordered)
