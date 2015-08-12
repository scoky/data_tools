#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findNumber
from group import Group,UnsortedInputGrouper

class ShareGroup(Group):
    def __init__(self, tup):
        super(ShareGroup, self).__init__(tup)

    def add(self, chunks):
        first = list(reversed(chunks[args.one].strip(args.separator).split(args.separator)))
        second = list(reversed(chunks[args.two].strip(args.separator).split(args.separator)))
        share = 0
        for f,s in zip(first,second):
            if f == s:
                share += 1
            else:
                break
        if args.append:
            args.outfile.write(args.jdelim.join(chunks) + args.jdelim)
        args.outfile.write(str(share) + '\n')

    def done(self):
        pass

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Compute share of column(s)')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-o', '--one', type=int, default=0)
    parser.add_argument('-t', '--two', type=int, default=1)
    parser.add_argument('-s', '--separator', default='.')
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    args = parser.parse_args()

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    grouper = UnsortedInputGrouper(args.infile, ShareGroup, [], args.delimiter)
    grouper.group()
