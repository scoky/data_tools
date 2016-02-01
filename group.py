#!/usr/bin/python

import os
import sys
import argparse

class Group(object):
    def __init__(self, tup):
        self.tup = tup
        
    def add(self, chunks):
        pass
        
    def done(self):
        pass

class SortedInputGrouper(object):
    def __init__(self, infile, group_cols=[0], delimiter=None):
        self.infile = infile
        self.group_cols = group_cols
        self.delimiter = delimiter
        self.tup = None
        self.chunks = None

    def group(self):
        line = self.infile.next()
        if not line:
            return
        
        self.chunks = line.rstrip().split(self.delimiter)
        self.tup = [self.chunks[g] for g in self.group_cols]
        while self.tup != None:
            yield self._gather()
                
    def _gather(self):
        # Yield the capture chunks
        yield self.chunks
        # Look for more matching the tuple
        for line in self.infile:
            self.chunks = line.rstrip().split(self.delimiter)
            ntup = [self.chunks[g] for g in self.group_cols]
            if ntup == self.tup:
                yield self.chunks
            else:
                self.tup = ntup
                return
        self.tup = None
    
class UnsortedInputGrouper(object):
    def __init__(self, infile, group_cls=Group, group_cols=[0], delimiter=None):
        self.infile = infile
        self.group_cols = group_cols
        self.delimiter = delimiter
        self.dict = {}
        self.group_cls = group_cls

    def group(self):
        jdelim = ' ' if not self.delimiter else self.delimiter
        keys = []
        for line in self.infile:
            chunks = line.rstrip().split(self.delimiter)
            tup = [chunks[g] for g in self.group_cols]
            key = jdelim.join(tup)
            if key not in self.dict:
                self.dict[key] = self.group_cls(tup)
                keys.append(key)
            self.dict[key].add(chunks)
        for key in keys:
            self.dict[key].done()
            
def run_grouping(infile, group_cls=Group, group_cols=[0], delimiter=None, ordered=False):
    if ordered:
        grouper = SortedInputGrouper(infile, group_cols, delimiter)
        for chunk in grouper.group():
            g = group_cls(grouper.tup)
            for item in chunk:
                g.add(item)
            g.done()
    else:
        UnsortedInputGrouper(infile, group_cls, group_cols, delimiter).group()


