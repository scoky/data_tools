#!/usr/bin/env python

import os
import sys
from data_tools.files import findNumber,ParameterParser
from data_tools.group import Group,run_grouping

class ShareGroup(Group):
    def __init__(self, tup):
        super(ShareGroup, self).__init__(tup)

    def add(self, chunks):
        first,second = [list(reversed(chunks[col].strip(args.separator).split(args.separator))) for col in args.columns]
        share = 0
        for f,s in zip(first,second):
            if f == s:
                share += 1
            else:
                break
        if args.append:
            args.outfile.write(chunks + [share])
        else:
            args.outfile.write(self.tup + [share])

    def done(self):
        pass

if __name__ == "__main__":
    pp = ParameterParser('Compute postfix share of column', columns = '*', labels = [None])
    pp.parser.add_argument('-s', '--separator', default='.')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = ['_'.join(args.columns_names) + '_postfix_share']
    args = pp.getArgs(args)
    if len(args.columns) != 2:
        raise Exception('Must specify exactly 2 columns!')

    run_grouping(args.infile, ShareGroup, args.group, args.ordered)
