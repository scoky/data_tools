#!/usr/bin/python

import os
import sys
import argparse
from input_handling import findNumber,FileReader,Header

class CollaterFile(object):
    def __init__(self, fstream, column, key, line, callback):
        self.fstream = fstream
        self.column = column
        self.key = key
        self.line = line
        self.callback = callback

class Collater(object):
    def __init__(self, numerical=True, delimiter=None):
        self.getKey = self.getNumKey if numerical else self.getStrKey
        self.delimiter = delimiter
        self.memory = []
        
    def addFile(self, fstream, callback, column=0):
        line = fstream.readline()
        # If there is nothing to read, drop the stream immediately
        if line:
            self.memory.append(CollaterFile(fstream, column, self.getKey(line, column), line, callback))
            
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
                f.key = self.getKey(f.line, f.column)
            # Else the file is done, remove it from memory
            else:
                del self.memory[i]
                
    def stop(self):
        self.run = False

    def getStrKey(self, line, col):
        return line.split(self.delimiter)[col]

    def getNumKey(self, line, col):
        return findNumber(line.split(self.delimiter)[col])
    
def printLine(line):
    args.outfile.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Collate multiple files')
    parser.add_argument('infiles', nargs='+', default=[sys.stdin])
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-n', '--numerical', default=False, action='store_true')
    parser.add_argument('-c', '--columns', nargs='+', default=[0])
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    if len(args.columns) == 1:
        args.columns = args.columns*len(args.infiles)
    if len(args.columns) != len(args.infiles):
        sys.stderr.write('InputError: invalid columns argument\n')
        exit()

    args.inheader = None
    collater = Collater(args.numerical)
    for col,infile in zip(args.columns, args.infiles):
        infile = FileReader(infile)
        if not args.inheader or len(args.inheader) == 0:
            args.inheader = infile.Header()
        col = infile.Header().index(col)
        collater.addFile(infile, printLine, col)
        
    if args.inheader:
        args.outfile.write(args.inheader.value())
    collater.run()

