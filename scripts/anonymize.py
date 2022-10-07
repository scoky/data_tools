#!/usr/bin/env python

import os
import sys
import argparse
from collections import defaultdict
from data_tools.files import ParameterParser,FileReader,FileWriter
from data_tools.group import Group,run_grouping

class AnonGroup(Group):
    def __init__(self, tup):
        super(AnonGroup, self).__init__(tup)
        self.reverse = {}
        self.forward = {}

    def add(self, chunks):
        for name,c in zip(args.columns_names, args.columns):
            if chunks[c] not in self.forward:
                # Find a non-colliding hash value
                val = abs(hash(chunks[c]))
                while val in self.reverse and self.reverse[val] != chunks[c]:
                    val = abs(val+1)

                self.reverse[val] = chunks[c]
                self.forward[chunks[c]] = str(val)
                
                # Write to mapping file
                if args.mapping:
                    args.mapping.write([name, chunks[c], self.forward[chunks[c]]])

            chunks[c] = self.forward[chunks[c]]
        args.outfile.write(chunks)

    def done(self):
        pass

class DeanonGroup(Group):
    def __init__(self, tup):
        super(DeanonGroup, self).__init__(tup)

    def add(self, chunks):
        for name,c in zip(args.columns_names, args.columns):
            val = args.map[name][chunks[c]]
            chunks[c] = val
        args.outfile.write(chunks)

    def done(self):
        pass

def readMapping(mapfile):
    mappings = defaultdict(dict)
    for chunks in mapfile:
        mappings[chunks[0]][chunks[2]] = chunks[1]
    return mappings

if __name__ == "__main__":
    pp = ParameterParser('Replace column(s) with hashes for anonymization', columns = '*', append = False, ordered = False, group = False)
    pp.parser.add_argument('-m', '--mapping', default=None)
    pp.parser.add_argument('-r', '--reverse', action='store_true', default=False)
    args = pp.parseArgs()
    args.append = True
    args = pp.getArgs(args)

    if args.mapping and not args.reverse:
        args.mapping = FileWriter(args.mapping, None, args)
        if args.infile.hasHeader:
            args.mapping.header.addCols(['column', 'value', 'anonymized'])
    elif args.mapping:
        with FileReader(args.mapping, args) as mapfile:
            args.map = readMapping(mapfile)

    if args.reverse:
        group = DeanonGroup
    else:
        group = AnonGroup
    run_grouping(args.infile, group, [], False)

