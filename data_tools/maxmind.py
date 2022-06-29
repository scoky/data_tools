#!/usr/bin/env python

import os
import sys
import argparse
from lib.files import ParameterParser
from lib.group import Group,run_grouping

class MaxMindGroup(Group):
    def __init__(self, tup):
        super(MaxMindGroup, self).__init__(tup)

    def add(self, chunks):
        v = args.reader.city(chunks[args.column])
        data = [v.city.names[args.locale] if args.locale in v.city.names else 'unknown', v.country.iso_code, v.continent.code, v.location.latitude, v.location.longitude, v.location.accuracy_radius]
        if args.append:
            args.outfile.write(chunks + data)
        else:
            args.outfile.write(self.tup + data)

    def done(self):
        pass

if __name__ == "__main__":
    pp = ParameterParser('Geolocate IP addresses using MaxMind', columns = 1, group = False, ordered = False)
    pp.parser.add_argument('--db', help='MaxMind City DB file', required=True)
    pp.parser.add_argument('--locale', default='en', help='How to represent the city')
    args = pp.parseArgs()
    args.labels = ['city', 'country', 'continent', 'latitude', 'longitude', 'accuracy']
    args = pp.getArgs(args)
    import geoip2.database
    args.reader = geoip2.database.Reader(args.db)
    run_grouping(args.infile, MaxMindGroup, [], True)

