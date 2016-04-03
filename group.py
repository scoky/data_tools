#!/usr/bin/env python

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
    def __init__(self, infile, group_cols=[0]):
        self.infile = infile
        self.group_cols = group_cols
        self.tup = None
        self.chunks = None

    def group(self):
        try:
            self.chunks = self.infile.next()
        except StopIteration:
            return
        self.tup = [self.chunks[g] for g in self.group_cols]
        while self.tup != None:
            yield self._gather()
                
    def _gather(self):
        # Yield the capture chunks
        yield self.chunks
        # Look for more matching the tuple
        for chunks in self.infile:
            self.chunks = chunks
            ntup = [self.chunks[g] for g in self.group_cols]
            if ntup == self.tup:
                yield self.chunks
            else:
                self.tup = ntup
                return
        self.tup = None
    
class UnsortedInputGrouper(object):
    def __init__(self, infile, group_cls=Group, group_cols=[0]):
        self.infile = infile
        self.group_cols = group_cols
        self.dict = {}
        self.group_cls = group_cls

    def group(self):
        for chunks in self.infile:
            tup = [chunks[g] for g in self.group_cols]
            key = tuple(tup)
            if key not in self.dict:
                self.dict[key] = self.group_cls(tup)
            self.dict[key].add(chunks)
        for value in self.dict.itervalues():
            value.done()
            
def run_grouping(infile, group_cls=Group, group_cols=[0], ordered=False):
    group_cols = infile.header.indexes(group_cols)
    if ordered:
        grouper = SortedInputGrouper(infile, group_cols)
        for chunk in grouper.group():
            g = group_cls(grouper.tup)
            for item in chunk:
                g.add(item)
            g.done()
    else:
        UnsortedInputGrouper(infile, group_cls, group_cols).group()


