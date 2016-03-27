#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,FileReader,Header
from group import Group,run_grouping


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
            args.outfile.write(args.infile.Delimiter().join(chunks) + args.infile.Delimiter())
        args.outfile.write(str(share) + '\n')

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute share of column(s)')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default=[0,1])
    parser.add_argument('-s', '--separator', default='.')
    parser.add_argument('-l', '--label', default=None)
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    parser.add_argument('--delimiter', default=None)
    parser.add_argument('--header', action='store_true', default=False)
    args = parser.parse_args()
    if len(args.columns) != 2:
        raise Exception('Must specify exactly 2 columns!')
    args.infile = FileReader(args.infile, args.header, args.delimiter)
    names = args.infile.Header().names(args.columns)

    if args.append:
        outheader = args.infile.Header().copy()
    else:
        outheader = Header(exists = args.header)
    if not args.label:
        args.label = '_'.join(names) + '_postfix_share'
    outheader.addCol(args.label)
    args.outfile.write(outheader.value(args.infile.Delimiter()))
    # Get columns for use in computation
    args.columns = args.infile.Header().indexes(args.columns)
    

    run_grouping(args.infile, ShareGroup, [], ordered = False)
