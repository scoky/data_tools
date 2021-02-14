#!/usr/bin/env python

import os
import sys
import argparse
from data_tools.files import findNumber,ParameterParser

class CollaterFile(object):
    def __init__(self, fstream, columns, key, line, callback):
        self.fstream = fstream
        self.columns = columns
        self.key = key
        self.line = line
        self.callback = callback

class Collater(object):
    def __init__(self, numerical=True):
        self.getKey = self.getNumKey if numerical else self.getStrKey
        self.memory = []
        
    def addFile(self, fstream, callback, columns=[0]):
        line = fstream.readline()
        # If there is nothing to read, drop the stream immediately
        if line:
            self.memory.append(CollaterFile(fstream, columns, self.getKey(line, columns), line, callback))
            
    def run(self):
        self.run = True
        while len(self.memory) > 0 and self.run:
            # Find the file with the minimum key
            i,f = min(enumerate(self.memory), key = lambda item: item[1].key)
            # Send the minimum line to the callback
            f.callback(f.line)
            # Get a new line to replace what was the minimum
            f.line = f.fstream.readline()
            # If there is a new line, update the key
            if f.line:
                f.key = self.getKey(f.line, f.columns)
            # Else the file is done, remove it from memory
            else:
                del self.memory[i]
                
    def stop(self):
        self.run = False

    def getStrKey(self, line, cols):
        return tuple(line[col] for col in cols)

    def getNumKey(self, line, cols):
        return tuple(findNumber(line[col]) for col in cols)
    
def printLine(line):
    args.outfile.write(line)

if __name__ == "__main__":
    pp = ParameterParser('Collate multiple files', columns = 0, infiles = '*', group = False, append = False, ordered = False)
    pp.parser.add_argument('-n', '--numerical', default=False, action='store_true')
    pp.parser.add_argument('-o', '--on', nargs='+', default=['0'], help='columns to join upon')
    args = pp.parseArgs()
    args = pp.getArgs(args)
    if len(args.on) == 1:
        args.on = args.on*len(args.infiles)
    if len(args.on) != len(args.infiles):
        raise Exception('InputError: invalid columns argument\n')
    cols = []
    for infile,c in zip(args.infiles, args.on):
        cols.append(infile.header.indexes(c.split('+')))
    args.on = cols

    collater = Collater(args.numerical)
    for cols,infile in zip(args.on, args.infiles):
        if len(args.outfile.header) == 0:
            args.outfile.header.addCols(infile.header.columns)
        cols = infile.header.indexes(cols)
        collater.addFile(infile, printLine, cols)

    collater.run()

