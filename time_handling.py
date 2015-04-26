#!/usr/bin/python

import os
import sys
import argparse
import traceback
from datetime import datetime,timedelta,time as dtime
from decimal import Decimal

def ToUnixTime(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = datetime(dt) - epoch
    return delta.days*86400 + delta.seconds

def ToDateTime(dt):
    return datetime.utcfromtimestamp(float(dt))
    
def TimeOfDay(dt):
    dt = ToDateTime(dt)
    tod = dtime(dt.hour, dt.minute, dt.second, dt.microsecond)
    return tod

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Time processing')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--column', type=int, default=0)
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    parser.add_argument('-f', '--function', choices=['ToUnixTime', 'ToDateTime', 'TimeOfDay'], default='ToDateTime')
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    args.function = getattr(sys.modules[__name__], args.function)

    jdelim = args.delimiter if args.delimiter != None else ' '
    for line in args.infile:
        val = line.rstrip().split(args.delimiter)[args.column]
        res = args.function(val)
        if args.append:
            args.outfile.write('%s%s' % (line.rstrip(), jdelim))
        args.outfile.write(str(res)+'\n')
    
