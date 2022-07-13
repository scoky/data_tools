#!/usr/bin/env python

import os
import sys
import argparse
from lib.files import ParameterParser,findNumber
from lib.group import Group,run_grouping

class GeoDistanceGroup(Group):
    def __init__(self, tup):
        super(GeoDistanceGroup, self).__init__(tup)

    def add(self, chunks):
        from geopy.distance import great_circle
        lat1 = findNumber(chunks[args.columns[0]])
        long1 = findNumber(chunks[args.columns[1]])
        lat2 = findNumber(chunks[args.columns[2]])
        long2 = findNumber(chunks[args.columns[3]])
        dist = great_circle((lat1,long1), (lat2,long2))
        if args.append:
            args.outfile.write(chunks + [dist.km])
        else:
            args.outfile.write(self.tup + [dist.km])

    def done(self):
        pass

if __name__ == "__main__":
    pp = ParameterParser('Calculate distance between two sets of coordinates', columns = 4, group = False, ordered = False)
    args = pp.parseArgs()
    args.labels = ['great_circle']
    args = pp.getArgs(args)
    run_grouping(args.infile, GeoDistanceGroup, [], True)

