#!/usr/bin/python

import os
import sys
import argparse
import traceback
from decimal import Decimal,InvalidOperation
from group import Group,run_grouping

class ResampleGroup(Group):
    def __init__(self, tup):
        super(ResampleGroup, self).__init__(tup)
        self.point = None

        self.jdelim = args.delimiter if args.delimiter != None else ' '
        self.prefix = ''
        if len(self.tup) > 0:
            self.prefix = self.jdelim.join(self.tup) + self.jdelim

    def add(self, chunks):
        npoint = (Decimal(chunks[args.xdata]), Decimal(chunks[args.ydata]))

        # Set up iteration
        if args.resample_file:
            self.pt_generator = ( v for v in args.resample_values )
        elif args.begin != None:
            self.pt_generator = nextpoint(args.begin, args.terminate, args.frequency)
        else:
            self.pt_generator = nextpoint(npoint[0], args.terminate, args.frequency)
        # First sample point
        try:
            self.x = self.pt_generator.next()
        except StopIteration:
            self.x = Decimal('inf')

        while self.x <= npoint[0]:
            args.outfile.write(self.prefix + str(self.x) + self.jdelim + str(npoint[1]) + '\n')
            try:
                self.x = self.pt_generator.next()
            except StopIteration:
                self.x = Decimal('inf')
        self.point = npoint

        self.add = self.addAfter

    def addAfter(self, chunks):
        npoint = (Decimal(chunks[args.xdata]), Decimal(chunks[args.ydata]))

        while self.x <= npoint[0]:
            y = args.interpolatef(self.point, npoint, self.x)    
            args.outfile.write(self.prefix + str(self.x) + self.jdelim + str(y) + '\n')
            try:
                self.x = self.pt_generator.next()
            except StopIteration:
                self.x = Decimal('inf')

        self.point = npoint

    def done(self):
        if not args.resample_file and (self.x == Decimal('inf') or args.terminate == None):
            return
        while True:
            args.outfile.write(self.prefix + str(self.x) + self.jdelim + str(self.point[1]) + '\n')
            try:
                self.x = self.pt_generator.next()
            except StopIteration:
                break


def interp_linear(p1, p2, x):
    try:
        return p1[1] + (p2[1] - p1[1]) * (x - p1[0]) / (p2[0] - p1[0])
    except InvalidOperation:
        return p1[1]   # p2[0] == p1[0]

def interp_step(p1, p2, x):
    return p1[1]

def nextpoint(b, t, f):
    x = b
    while t == None or x <= t:
        yield x
        x += f

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Resample the data points with a different frequency')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-f', '--frequency', type=Decimal, default=Decimal('1'))
    parser.add_argument('-i', '--interpolate', choices=['linear', 'step'], default='linear')
    parser.add_argument('-b', '--begin', type=Decimal, default=None, help='value to begin resampling at')
    parser.add_argument('-t', '--terminate', type=Decimal, default=None, help='value to terminate resampling at')
    parser.add_argument('-r', '--resample_file', type=argparse.FileType('r'), default=None, help='File to read resample points from')
    parser.add_argument('-e', '--resample_index', type=int, default=0)
    parser.add_argument('-x', '--xdata', type=int, default=0)
    parser.add_argument('-y', '--ydata', type=int, default=1)
    parser.add_argument('-g', '--group', nargs='+', type=int, default=[])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()

    if args.begin and args.resample_file:
        raise Exception('Cannot specify both file and begin parameters')
    elif args.resample_file:
        args.resample_values = [Decimal(line.rstrip().split()[args.resample_index]) for line in args.resample_file]
        args.resample_file.close()
    args.interpolatef = getattr(sys.modules[__name__], 'interp_'+args.interpolate)

    run_grouping(args.infile, ResampleGroup, args.group, args.delimiter, args.ordered)

