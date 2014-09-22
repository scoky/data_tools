#!/usr/bin/python

import logging
import argparse
import sys
import traceback
import os
import copy
from decimal import Decimal
from math import sqrt
from math import pow

class Command(object):
	def __init__(self, init, on_row, on_finish):
		self.init = init
		self.on_row = on_row
		self.on_finish = on_finish

class PerformReturn(object):
	def __init__(self, action):
		self.action = action

	def perform(self, a,b):
		self.action(a,b)
		return a

commands = {
'max' : 	Command(0, lambda a,b: max(a,Decimal(b)), lambda a: str(a)),
'min' : 	Command(sys.maxint, lambda a,b: min(a, Decimal(b)), lambda a: str(a)),
'mean' : 	Command([], PerformReturn(lambda a,b: a.append(Decimal(b))).perform, lambda a: str(sum(a)/len(a))),
'sum' : 	Command(0, lambda a,b: a+Decimal(b), lambda a: str(a)),
'count' : 	Command(0, lambda a,b: a+1, lambda a: str(a)),
'unique' : 	Command(set(), PerformReturn(lambda a,b: a.add(b)).perform, lambda a: str(len(a))),
'aggregate' : 	Command([], PerformReturn(lambda a,b: a.append(b)).perform, lambda a: ' '.join(a)),
#,
#'distribution' : Command([], PerformReturn(lambda a,b: a.append(Decimal(b))).perform, lambda a: str(
}


def group(infile, outfile, group_col, action, action_col, delimiter):
	command = commands[action]
	groups = {}
	for line in infile:
           try:
		chunks = line.rstrip().split(delimiter)
		g = chunks[group_col]
		if g not in groups:
			groups[g] = copy.copy(command.init)

		groups[g] = command.on_row(groups[g], chunks[action_col])
	   except Exception as e:
           	logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())
		
	for key in sorted(groups.keys()):
		outfile.write(key+delimiter+command.on_finish(groups[key])+'\n')
		

def main():
    group(args.infile, args.outfile, args.group_col, args.action, args.action_col, args.delimiter)

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Group rows by a given column value and perform an operation on the group')
    parser.add_argument('group_col', type=int, default=0, help='Column to group upon')
    parser.add_argument('action', choices=commands.keys(), help='Action to perform')
    parser.add_argument('action_col', nargs='?', type=int, default=0, help='Column to act upon')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help='only print errors')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print debug info. --quiet wins if both are present')
    args = parser.parse_args()

    # set up logging
    if args.quiet:
        level = logging.WARNING
    elif args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(
        format = "%(levelname) -10s %(asctime)s %(module)s:%(lineno) -7s %(message)s",
        level = level
    )

    main()

