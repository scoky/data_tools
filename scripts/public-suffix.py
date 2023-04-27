#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.files import findNumber,ParameterParser
from data_tools.group import Group,run_grouping

class WindowGroup(Group):
    def __init__(self, tup):
        super(WindowGroup, self).__init__(tup)

    def add(self, chunks):
        name = chunks[args.column].rstrip('.') # Remove the root .
        pub = args.psl.publicsuffix(name)
        if pub is None:
            pub = ''
            pub_prefix = name
        else:
            pub_prefix = name.split(pub, 1)[0].rstrip('.')
        pri = args.psl.privatesuffix(name)
        if pri is None:
            pri = pub
            pri_prefix = pub_prefix
        else:
            pri_prefix = name.split(pri, 1)[0].rstrip('.')
        vals = [pub_prefix, pub, pri_prefix, pri]
        if args.append:
            args.outfile.write(chunks + vals)
        else:
            args.outfile.write(self.tup + vals)

    def done(self):
        pass

if __name__ == "__main__":
    pp = ParameterParser('Get public suffix', columns = 1, labels = [None], group = False, ordered = False)
    pp.parser.add_argument('-s', '--suffix', default = None, help = 'if not specified, uses builtin from publicsuffixlist lib')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_prefix', args.column_name + '_suffix', args.column_name + '_prefix-1', args.column_name + '_suffix+1']
    args = pp.getArgs(args)

    from publicsuffixlist import PublicSuffixList
    if args.suffix is None:
        args.psl = PublicSuffixList()
    else:
        with open (args.suffix, 'rb') as f:
            args.psl = PublicSuffixList(f)

    run_grouping(args.infile, WindowGroup, [], False)

