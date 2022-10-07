#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.files import ParameterParser
from data_tools.group import Group,run_grouping

class MaxMindGroup(Group):
    def __init__(self, tup):
        super(MaxMindGroup, self).__init__(tup)

    def add(self, chunks):
        import geoip2.errors
        try:
            v = args.maxmind_function(chunks[args.column])
            data = [v.city.names[args.locale] if args.locale in v.city.names else 'unknown', v.city.confidence, v.country.iso_code, v.country.confidence, v.continent.code, v.location.latitude, v.location.longitude, v.location.accuracy_radius]
        except geoip2.errors.AddressNotFoundError:
            data = ['missing', None, 'missing', None, 'missing', 'missing', 'missing', None]
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
    args.labels = ['city', 'city_confidence', 'country', 'country_confidence', 'continent', 'latitude', 'longitude', 'accuracy']
    args = pp.getArgs(args)
    import geoip2.database
    args.reader = geoip2.database.Reader(args.db)
    if args.reader._db_type == 'GeoIP2-Enterprise':
        args.maxmind_function = args.reader.enterprise
    elif args.reader._db_type == 'GeoLite2-City':
        args.maxmind_function = args.reader.city
    run_grouping(args.infile, MaxMindGroup, [], True)

