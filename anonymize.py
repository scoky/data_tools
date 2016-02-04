#!/usr/bin/python

import os
import sys
import argparse
from decimal import Decimal
from collections import defaultdict
from input_handling import findNumber,FileReader,Header,openFile
from group import Group,run_grouping

class AnonGroup(Group):
    def __init__(self, tup):
        super(AnonGroup, self).__init__(tup)
        self.reverse = {}
        self.forward = {}

    def add(self, chunks):
        for name,c in zip(args.colNames, args.columns):
            if chunks[c] not in self.forward:
                # Find a non-colliding hash value
                val = abs(hash(chunks[c]))
                while val in self.reverse and self.reverse[val] != chunks[c]:
                    val = abs(val+1)

                self.reverse[val] = chunks[c]
                self.forward[chunks[c]] = str(val)
                
                # Write to mapping file
                if args.mapping:
                    args.mapping.write(args.jdelim.join((name, chunks[c], self.forward[chunks[c]])) + '\n')

            chunks[c] = self.forward[chunks[c]]
        args.outfile.write(args.jdelim.join(chunks) + '\n')

    def done(self):
        pass

class DeanonGroup(Group):
    def __init__(self, tup):
        super(DeanonGroup, self).__init__(tup)

    def add(self, chunks):
        for name,c in zip(args.colNames, args.columns):
            val = args.map[name][chunks[c]]
            chunks[c] = val

        args.outfile.write(args.jdelim.join(chunks) + '\n')

    def done(self):
        pass

def readMapping(mapfile, colName, value, anon):
    mappings = defaultdict(dict)
    for line in mapfile:
        chunks = line.rstrip().split()
        mappings[chunks[colName]][chunks[anon]] = chunks[value]
    return mappings

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Replace column(s) with hashes for anonymization')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-m', '--mapping', default=None)
    parser.add_argument('-c', '--columns', nargs='+', default=[0])
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-r', '--reverse', action='store_true', default=False)
    parser.add_argument('-o', '--ordered', action='store_true', default=False, help='input is sorted by group')
    args = parser.parse_args()
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    args.outheader = args.inheader.copy()
    if args.mapping and not args.reverse:
        args.mapheader = Header()
        args.mapheader.addCol('col')
        args.mapheader.addCol('value')
        args.mapheader.addCol('anonymized')
        args.mapping = openFile(args.mapping, 'w')
        args.mapping.write(args.mapheader.value())
    elif args.mapping:
        args.mapping = FileReader(args.mapping)
        args.mapheader = args.mapping.Header()
        args.map = readMapping(args.mapping, args.mapheader.index('col'), args.mapheader.index('value'), args.mapheader.index('anonymized'))
        args.mapping.close()
        
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.colNames = args.inheader.names(args.columns)
    args.columns = args.inheader.indexes(args.columns)

    args.jdelim = args.delimiter if args.delimiter != None else ' '
    if args.reverse:
        group = DeanonGroup
    else:
        group = AnonGroup
    run_grouping(args.infile, group, [], args.delimiter, args.ordered)

