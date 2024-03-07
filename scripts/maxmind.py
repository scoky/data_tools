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
        ip = chunks[args.column]
        import geoip2.errors
        try:
            v = args.maxmind_function(ip)
            data = []
            for f in args.fields:
                data.append(getField(f, v))
        except geoip2.errors.AddressNotFoundError:
            data = [None] * len(args.fields)
        if args.append:
            args.outfile.write(chunks + data)
        else:
            args.outfile.write(self.tup + data)

    def done(self):
        pass

def getField(f, v):
    from geoip2.models import ASN,Enterprise,City
    try:
        if f == 'asn':
            if type(v) == ASN:
                return v.autonomous_system_number
            else:
                return v.traits.autonomous_system_number
        elif f == 'org':
            if type(v) == ASN:
                return v.autonomous_system_organization
            else:
                return v.traits.autonomous_system_organization
        elif f == 'city':
            return v.city.names[args.locale] if args.locale in v.city.names else 'unknown'
        elif f == 'city_confidence':
            return v.city.confidence
        elif f == 'country':
            return v.country.iso_code
        elif f == 'country_confidence':
            return v.country.confidence
        elif f == 'continent':
            return v.continent.code
        elif f == 'latitude':
            return v.location.latitude
        elif f == 'longitude':
            return v.location.longitude
        elif f == 'accuracy':
            return v.location.accuracy_radius
    except AttributeError:
        return 'unknown'

if __name__ == "__main__":
    pp = ParameterParser('Geolocate IP addresses using MaxMind', columns = 1, group = False, ordered = False)
    pp.parser.add_argument('--db', help='MaxMind City DB file', required=True)
    pp.parser.add_argument('--locale', default='en', help='How to represent the city')
    pp.parser.add_argument('-f', '--fields', choices=['asn', 'org', 'city', 'city_confidence', 'country', 'country_confidence', 'continent', 'latitude', 'longitude', 'accuracy'], default=['asn', 'org', 'city', 'city_confidence', 'country', 'country_confidence', 'continent', 'latitude', 'longitude', 'accuracy'], nargs="+")
    args = pp.parseArgs()
    args.labels = args.fields
    args = pp.getArgs(args)
    import geoip2.database
    args.reader = geoip2.database.Reader(args.db)
    if args.reader._db_type == 'GeoIP2-Enterprise':
        args.maxmind_function = args.reader.enterprise
    elif args.reader._db_type == 'GeoLite2-City':
        args.maxmind_function = args.reader.city
    elif args.reader._db_type == 'GeoLite2-ASN':
        args.maxmind_function = args.reader.asn
    run_grouping(args.infile, MaxMindGroup, [], True)

