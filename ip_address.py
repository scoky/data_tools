#!/usr/bin/env python

import os
import sys
import argparse
from input_handling import findIPAddress,FileReader,Header

class IPRange(object):
    def __init__(self, start, end=None, mask=None):
        if (not end and not mask) or (end and mask):
            raise Exception('Must specify either end IP address or mask')
        self.start = start
        self.end = end
        if mask:
            self.end = IPRange.mask(start, mask) | 1 << (32 - mask)
            
    def in_range(self, ip):
        return ip > self.start and ip < self.end
        
    @classmethod
    def mask(cls, ip, mask):
        mask = (1 << 32) - (1 << 32 >> mask)
        return int(ip) & mask

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Parse input based upon available functions')
    parser.add_argument('infile', nargs='?', default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default=[0])
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    parser.add_argument('-f', '--function', choices=['mask'], default='mask')
    parser.add_argument('-s', '--slash', type=int, default=24)
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    args.infile = FileReader(args.infile)

    # Get the header from the input file if there is one
    args.inheader = args.infile.Header()
    # Setup output header
    if args.append:
        args.outheader = args.inheader.copy()
    else:
        args.outheader = Header()
    for col in args.columns:
        args.outheader.addCol(args.inheader.name(col) + '_' + args.function)
    # Write output header
    args.outfile.write(args.outheader.value())
    # Get columns for use in computation
    args.columns = args.inheader.indexes(args.columns)
    args.function = getattr(IPRange, args.function)

    jdelim = args.delimiter if args.delimiter != None else ' '
    for line in args.infile:
        chunks = line.rstrip().split(args.delimiter)
        vals = [args.function(findIPAddress(chunks[i]), args.slash) for i in args.columns]
        if args.append:
            args.outfile.write('%s%s' % (line.rstrip(), jdelim))
        args.outfile.write(jdelim.join(map(str,vals))+'\n')
