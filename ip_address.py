#!/usr/bin/python

import os
import sys
import argparse
import traceback
from input_handling import findIPAddress

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
                                     description='Parse input base upon available functions')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    parser.add_argument('-f', '--function', choices=['mask'], default='mask')
    parser.add_argument('-s', '--slash', type=int, default=24)
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    args.function = getattr(IPRange, args.function)

    jdelim = args.delimiter if args.delimiter != None else ' '
    for line in args.infile:
        chunks = line.rstrip().split(args.delimiter)
        vals = [args.function(findIPAddress(chunks[i]), args.slash) for i in args.columns]
        if args.append:
            args.outfile.write('%s%s' % (line.rstrip(), jdelim))
        args.outfile.write(jdelim.join(map(str,vals))+'\n')
