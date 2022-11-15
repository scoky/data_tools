#!/usr/bin/env python

import os
import sys
import random
from collections import defaultdict
from data_tools.files import ParameterParser
from data_tools.group import Group,run_grouping

class SampleGroup(Group):
    def __init__(self, tup):
        super(SampleGroup, self).__init__(tup)
        self.row = []
        self._count = 0
        if args.append:
            self.rows = defaultdict(list)
            self.add = self.addRow
        if args.probability:
            self.done = self.noaction
            self.add = self.sampleRow

    def add(self, chunks):
        val = chunks[args.column]
        self.row.append(val)

    def addRow(self, chunks):
        val = chunks[args.column]
        self.row.append(val)
        self.rows[val].append(chunks)

    def sampleRow(self, chunks):
        val = chunks[args.column]
        if random.random() <= args.probability and self._count < args.number:
            self._count += 1
            if args.append:
                args.outfile.write(chunks)
            else:
                args.outfile.write(self.tup + [val])

    def done(self):
        if args.replacement:
            for val in (random.choice(self.row) for n in range(args.number)):
                if args.append:
                    args.outfile.write(random.choice(self.rows[val]))
                else:
                    args.outfile.write(self.tup + [val])
        else:
            for val in self.sample(self.row, args.number):
                if args.append:
                    i = random.choice(list(range(len(self.rows[val]))))
                    args.outfile.write(self.rows[val][i])
                    del self.rows[val][i]
                else:
                    args.outfile.write(self.tup + [val])

    def sample(self, rows, number):
        if number >= len(rows):
            return rows
        else:
            return random.sample(rows, number)

    def noaction(self):
        pass

if __name__ == "__main__":
    pp = ParameterParser('Sample rows from file', columns = 1)
    pp.parser.add_argument('-r', '--replacement', action='store_true', default=False, help='with replacement')
    pp.parser.add_argument('-s', '--seed', type=int, default=12345)
    pp.parser.add_argument('-n', '--number', type=int, default=10, help='number of samples')
    pp.parser.add_argument('-p', '--probability', type=float, default=None, help='use probability to sample values, rather than choice. advantage is lower memory consumption. disadvantage is may not get [number] samples and uneven distribution.')
    args = pp.parseArgs()
    args = pp.getArgs(args)

    random.seed(args.seed)
    run_grouping(args.infile, SampleGroup, args.group, args.ordered)
