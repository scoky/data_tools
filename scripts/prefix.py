#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.files import ParameterParser
from data_tools.group import Group,run_grouping
import ipaddress

class PrefixGroup(Group):
    def __init__(self, tup):
        super(PrefixGroup, self).__init__(tup)

    def add(self, chunks):
        vals = []
        for c in args.columns:
            ip = ipaddress.ip_network(str(chunks[c]))
            plen = args.ipv4
            if ip.version == 6:
                plen = args.ipv6
            vals.append(str(ip.supernet(new_prefix = plen)))
        args.outfile.write(chunks + vals)

    def done(self):
        pass

if __name__ == "__main__":
    pp = ParameterParser('Compute prefixes of IP addresses', columns = '*', group = False, append = False, labels = [None], ordered = False)
    pp.parser.add_argument('-i', '--ipv4', default=24, type=int, help='length to subnet IPv4 addresses')
    pp.parser.add_argument('-p', '--ipv6', default=48, type=int, help='length of subnet IPv6 addresses')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [cn + '_prefix' for cn in args.columns_names]
    args = pp.getArgs(args)

    run_grouping(args.infile, PrefixGroup, [], False)
