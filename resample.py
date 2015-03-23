#!/usr/bin/python

import os
import sys
import argparse
import traceback
from decimal import Decimal
from group import Group,UnsortedInputGrouper

class ResampleGroup(Group):
    def __init__(self, tup):
        super(ResampleGroup, self).__init__(tup)
        self.point = None
        self.jdelim = args.delimiter if args.delimiter != None else ' '

    def add(self, chunks):
        npoint = (Decimal(chunks[args.xdata]), Decimal(chunks[args.ydata]))
        if self.point:
            while npoint[0] > self.x:
                y = args.interpolatef(self.point, npoint, self.x)
                if len(self.tup) > 0:
                    args.outfile.write(jdelim.join(self.tup) + jdelim)
                args.outfile.write(str(self.x) + self.jdelim + str(y) + '\n')
                self.x += args.frequency
        else:
            if args.sync or (npoint[0] % args.frequency) == 0:
                self.x = npoint[0]
            else:
                self.x = npoint[0] - (npoint[0] % args.frequency) + args.frequency
        self.point = npoint

    def done(self):
        pass

def linear(p1, p2, x):
    return p1[1] + (p2[1] - p1[1]) * (x - p1[0]) / (p2[0] - p1[0])

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Resample the data points with a different frequency')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-f', '--frequency', type=Decimal, default=Decimal('1'))
    parser.add_argument('-i', '--interpolate', choices=['linear'], default='linear')
    parser.add_argument('-s', '--sync', action='store_true', default=False)
    parser.add_argument('-x', '--xdata', type=int, default=0)
    parser.add_argument('-y', '--ydata', type=int, default=1)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    args.interpolatef = getattr(sys.modules[__name__], args.interpolate)
    
    grouper = UnsortedInputGrouper(args.infile, ResampleGroup, args.group, args.delimiter)
    grouper.group()
