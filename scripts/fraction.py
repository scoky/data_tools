#!/usr/bin/env python

import os
import sys
import argparse
from collections import defaultdict
from data_tools.files import findNumber,ParameterParser
from data_tools.group import Group,run_grouping

class FractionGroup(Group):
    def __init__(self, tup):
        super(FractionGroup, self).__init__(tup)
        self.rows = defaultdict(int)
        self.total = 0
        self.add = self._add
        self.done = self._done
        if args.append:
            self.fullrows = defaultdict(list)
            self.add = self.addrow
            self.done = self.donerow
        
    def _add(self, chunks):
        num = findNumber(chunks[args.column])
        self.rows[num] += 1
        self.total += num
    
    def addrow(self, chunks):
        num = findNumber(chunks[args.column])
        self.rows[num] += 1
        self.total += num
        self.fullrows[num].append(chunks)
        
    def donerow(self):
        for r in self.rows.keys():
            for row in self.fullrows[r]:
                args.outfile.write(row + [r / self.total])

    def _done(self):
        for r,c in self.rows.items():
            for i in range(c):
                args.outfile.write(self.tup + [r / self.total])

if __name__ == "__main__":
    pp = ParameterParser('Compute fraction of column sum', columns = 1, labels = [None])
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = [args.column_name + '_fraction']
    args = pp.getArgs(args)
    
    run_grouping(args.infile, FractionGroup, args.group, args.ordered)

