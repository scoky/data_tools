#!/usr/bin/python

import os
import sys
import argparse
from collections import defaultdict
from input_handling import FileReader,Header

class join(object):
    def __init__(self):
        self.values = defaultdict(list)

    def add(self, key, i, line):
        if len(self.values[i]) > 0:
            sys.stderr.write('Warning: duplicate key detected in merge: %s\n' % key)
        self.values[i].append(line)

    def fill(self, i, count):
        if len(self.values[i]) == 0:
            self.values[i].append(args.jdelim.join(map(str, [None]*count)))

    def remove(self):
        for values in self.values.itervalues():
            if len(values) > 0:
                del values[0]

    def __len__(self):
        count = 0
        for values in self.values.itervalues():
            if len(values) > 0:
                count += 1
        return count
        
    def output(self):
        return args.jdelim.join(line[0] for j,line in sorted(self.values.iteritems(), key = lambda i: i[0])) + '\n'

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Merge files on column(s)')
    parser.add_argument('infiles', nargs='*', default=[sys.stdin])
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', default=['0'], help='use + to specify multiple columns per file')
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-i', '--inner', action='store_true', default=False, help='inner merge')
    args = parser.parse_args()
    if len(args.columns) == 1:
        args.columns = args.columns*len(args.infiles)
    if len(args.columns) != len(args.infiles):
        sys.stderr.write('InputError: invalid columns argument\n')
        exit()
    cols = []
    for c in args.columns:
        cols.append(c.split('+'))
    args.columns = cols

    args.infiles = [FileReader(infile) for infile in args.infiles]
    inheaders = [infile.Header() for infile in args.infiles]
        
    args.jdelim = args.delimiter if args.delimiter != None else ' '
    merge = defaultdict(join)        
    outheader = Header()
    outheader.extend(inheaders[0])
    for i,tup in enumerate(zip(args.infiles[1:], args.columns[1:], inheaders[1:])):
        i += 1
        infile,col,inheader = tup
        col = inheader.indexes(col)
        outheader.extend(inheader)
        for line in infile:
            line = line.rstrip()
            keys = line.split(args.delimiter)
            key = args.jdelim.join([keys[c] for c in col])
            merge[key].add(key, i, line)
        infile.close()

    args.outfile.write(outheader.value())
    col = inheaders[0].indexes(args.columns[0])
    for line in args.infiles[0]:
        line = line.rstrip()
        keys = line.split(args.delimiter)
        key = args.jdelim.join([keys[c] for c in col])
        merge[key].add(key, 0, line)
        if len(merge[key]) == len(args.infiles) or not args.inner:
            for i in range(1, len(args.infiles)):
                merge[key].fill(i, len(inheaders[i]))
            args.outfile.write(merge[key].output())
            merge[key].remove()

    if not args.inner:
        for j in merge.itervalues():
            while len(j) > 0:
                for i in range(len(args.infiles)):
                    j.fill(i, len(inheaders[i]))
                args.outfile.write(j.output())
                j.remove()
