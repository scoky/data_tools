#!/usr/bin/env python

import os
import sys
from data_tools.files import ParameterParser
from datetime import datetime,timedelta,time as dtime
from decimal import Decimal
import time
from data_tools.group import Group,run_grouping

class TimestampGroup(Group):
    def __init__(self, tup):
        super(TimestampGroup, self).__init__(tup)

    def add(self, chunks):
        timestamp = ' '.join([chunks[i] for i in args.columns])
        if args.in_format is None: 
            timestamp = datetime.utcfromtimestamp(float(timestamp))
        else:
            timestamp = datetime.strptime(timestamp, args.in_format)
        if args.out_format is None:
            timestamp = time.mktime(timestamp.timetuple())
        else:
            timestamp = timestamp.strftime(args.out_format)
        args.outfile.write(chunks + [timestamp])

    def done(self):
        pass

def ToUnixTime(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.days*86400 + delta.seconds

def ToDateTime(dt):
    return datetime.utcfromtimestamp(dt)
    
def TimeOfDay(dt):
    tod = dtime(dt.hour, dt.minute, dt.second, dt.microsecond)
    return tod
    
def cToUnixTime(dt):
    return ToUnixTime(datetime.strptime(dt, args.format))
    
def cToDateTime(dt):
    return ToDateTime(float(dt)).strftime(args.format)
    
def cTimeOfDay(dt):
    return TimeOfDay(ToDateTime(float(dt))).strftime(args.format)

if __name__ == "__main__":
    pp = ParameterParser('Convert timestamps', columns = '*', group = False, append = False, ordered = False)
    pp.parser.add_argument('-i', '--in-format')
    pp.parser.add_argument('-o', '--out-format')
    args = pp.parseArgs()
    args.append = True
    args = pp.getArgs(args)
    run_grouping(args.infile, TimestampGroup, [], False)
    # args.function = getattr(sys.modules[__name__], 'c'+args.function)
    # if not args.format:
    #     if args.function == cTimeOfDay:
    #         args.format = '%H:%M:%S.%f'
    #     else: 
    #         args.format = '%Y-%m-%d_%H:%M:%S.%f'
    # 
    # jdelim = args.delimiter if args.delimiter != None else ' '
    # for line in args.infile:
    #     val = line.rstrip().split(args.delimiter)[args.column]
    #     res = args.function(val)
    #     if args.append:
    #         args.outfile.write('%s%s' % (line.rstrip(), jdelim))
    #     args.outfile.write(str(res)+'\n')
    
