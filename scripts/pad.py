#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.files import FileReader,ParameterParser
from data_tools.group import Group,run_grouping

class PadGroup(Group):
    def __init__(self, tup):
        super(PadGroup, self).__init__(tup)
        self.present = set()
        self.ncolumns = 0

    def add(self, chunks):
        self.present.add(tuple(chunks[i] for i in args.columns))
        args.outfile.write(chunks)
        self.ncolumns = len(chunks)

    def done(self):
        row = (args.pad * self.ncolumns)[:self.ncolumns]
        for element in args.elements:
            if element not in self.present:
                for i,j in enumerate(args.columns):
                    row[j] = element[i]
                for i,j in enumerate(args.group):
                    row[j] = self.tup[i]
                args.outfile.write(row)

if __name__ == "__main__":
    pp = ParameterParser('Generate additional rows to pad input', columns = '*', append = False, labels = False, ordered = False)
    pp.parser.add_argument('-e', '--elements', help='File containing list elements, one per line.')
    pp.parser.add_argument('-p', '--pad', nargs='+', default=['0'])
    args = pp.parseArgs()
    args.append = True
    args = pp.getArgs(args)

    elements = set()
    with FileReader(args.elements, args) as f:
        for chunks in f:
            elements.add(tuple(chunks))
    args.elements = elements

    run_grouping(args.infile, PadGroup, args.group, ordered = False)
