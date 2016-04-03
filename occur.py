#!/usr/bin/env python

import os
import sys
import argparse
from input_handling import ParameterParser
from group import Group,run_grouping

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
        self.add = self.addNothing
        
    def addNothing(self, chunks):
        self.last = chunks

    def done(self):
        if self.last is not None and 'last' in args.order:
            args.outfile.write(self.last)

if __name__ == "__main__":
    pp = ParameterParser('Output the first/last occurance of a group', columns = False, append = False, ordered = False)
    pp.parser.add_argument('-o', '--order', nargs='+', default=['first'], choices=['first', 'last'])
    args = pp.parseArgs()
    args.append = True
    args = pp.getArgs(args)

    run_grouping(args.infile, OccurGroup, args.group, False)
