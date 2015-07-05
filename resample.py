#!/usr/bin/python

import os
import sys
import argparse
import traceback
from decimal import Decimal,InvalidOperation
from group import Group,UnsortedInputGrouper

class ResampleGroup(Group):
    def __init__(self, tup):
        super(ResampleGroup, self).__init__(tup)
        self.point = None
        self.jdelim = args.delimiter if args.delimiter != None else ' '

    def add(self, chunks):
        npoint = (Decimal(chunks[args.xdata]), Decimal(chunks[args.ydata]))
        
        if args.begin:
            self.x = args.begin
            while self.x < npoint[0]:
                if len(self.tup) > 0:
                    args.outfile.write(self.jdelim.join(self.tup) + self.jdelim)
                args.outfile.write(str(self.x) + self.jdelim + str(npoint[1]) + '\n')
                self.x += args.frequency

        elif args.sync or (npoint[0] % args.frequency) == 0:
            self.x = npoint[0]
        else:
            self.x = npoint[0] - (npoint[0] % args.frequency) + args.frequency
        self.point = npoint
        if args.expand:
            self.add = self.addAfterExpand
        else:
            self.add = self.addAfter

    def addAfter(self, chunks):
        if args.terminate and self.x > args.terminate:
            self.add = addNothing
            return

        npoint = (Decimal(chunks[args.xdata]), Decimal(chunks[args.ydata]))
        if npoint[0] >= self.x:
            y = args.interpolatef(self.point, npoint, self.x)

            if len(self.tup) > 0:
                args.outfile.write(self.jdelim.join(self.tup) + self.jdelim)
            args.outfile.write(str(self.x) + self.jdelim + str(y) + '\n')

            if self.x != npoint[0] and (npoint[0] % args.frequency) == 0:
                self.x = npoint[0]
            else:
                self.x = npoint[0] - (npoint[0] % args.frequency) + args.frequency
        self.point = npoint

    def addAfterExpand(self, chunks):
        if args.terminate and self.x > args.terminate:
            self.add = addNothing
            return

        npoint = (Decimal(chunks[args.xdata]), Decimal(chunks[args.ydata]))
        if npoint[0] >= self.x:
            # Unwind to compute first two points, so future points can be computed via deltas
            y = args.interpolatef(self.point, npoint, self.x)
            yd = args.interpolatef(self.point, npoint, self.x + args.frequency) - y
            while npoint[0] >= self.x:
                if len(self.tup) > 0:
                    args.outfile.write(self.jdelim.join(self.tup) + self.jdelim)
                args.outfile.write(str(self.x) + self.jdelim + str(y) + '\n')
                self.x += args.frequency
                y += yd
        self.point = npoint

    def addNothing(self, chunks):
        pass

    def done(self):
        while args.terminate and self.x <= args.terminate:
            if len(self.tup) > 0:
                args.outfile.write(self.jdelim.join(self.tup) + self.jdelim)
            args.outfile.write(str(self.x) + self.jdelim + str(self.point[1]) + '\n')
            self.x += args.frequency


def interp_linear(p1, p2, x):
    try:
        return p1[1] + (p2[1] - p1[1]) * (x - p1[0]) / (p2[0] - p1[0])
    except InvalidOperation:
        return p1[1]   # p2[0] == p1[0]

def interp_none(p1, p2, x):
    return p1[1]

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Resample the data points with a different frequency')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-f', '--frequency', type=Decimal, default=Decimal('1'))
    parser.add_argument('-i', '--interpolate', choices=['linear', 'none'], default='linear')
    parser.add_argument('-s', '--sync', action='store_true', default=False)
    parser.add_argument('-b', '--begin', type=Decimal, default=None, help='value to begin resampling at')
    parser.add_argument('-t', '--terminate', type=Decimal, default=None, help='value to terminate resampling at')
    parser.add_argument('-e', '--expand', action='store_true', default=False)
    parser.add_argument('-x', '--xdata', type=int, default=0)
    parser.add_argument('-y', '--ydata', type=int, default=1)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    if args.begin and args.sync:
        raise Exception('Cannot specify both sync and begin parameters')
    args.interpolatef = getattr(sys.modules[__name__], 'interp_'+args.interpolate)
    
    grouper = UnsortedInputGrouper(args.infile, ResampleGroup, args.group, args.delimiter)
    grouper.group()
