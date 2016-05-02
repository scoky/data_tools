#!/usr/bin/env python

import os,sys,argparse
sys.path.insert(1, os.path.join(os.path.dirname(__file__), os.pardir))
from toollib.files import ParameterParser
from toollib.group import Group,run_grouping
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()
import numpy as np

class PlotGroup(Group):
    def __init__(self, tup):
        super(PlotGroup, self).__init__(tup)
        self.data = []
        
    def add(self, chunks):
        num = findNumber(chunks[args.column])
        self.rows[num] += 1
        self.total += num

    def done(self):
        pass # Display it here

def present(value):
    return value and len(value) > 0
    
class Mapping(object):
    def __init__(self, variable, vtype):
        self.variable = variable
        self.vtype = vtype
  
class Source(object):
    def __init__(self, data):
        self.maps = {}
        self.data = data

    def get(self, v):
        if v in self.maps:
            return [d[self.maps[v]] for d in self.data]
        else:
            raise IndexError('No mapping for {0} in source!'.format(v))
            
def mappings(args):
    try:
        parts = (' '.join(args.mapping)).split('=')
        maps = {}

        v = parts[0].strip()
        for part in parts[1:-1]:
            m, v_next = part.rsplit(None, 1)
            maps[v] = [None if m1.strip() == '' else m1.strip() for m1 in m.split(',')]
            v = v_next.strip()
        maps[v] = [None if m1.strip() == '' else m1.strip() for m1 in parts[-1].split(',')]
        return maps
    except Exception as e:
        raise ValueError('Invalid mapping', e)
            
def fmt(value, vtype, vformat):
    try:
        if vtype == 'int':
            return int(value)
        elif vtype == 'float':
            return float(value)
        elif vtype == 'datetime':
            return datetime.strptime(value, vformat)
    except Exception as e:
        raise ValueError('Input value error ({0} {1] {2])'.format(value, vtype, vformat), e)

if __name__ == "__main__":
    pp = ParameterParser('Plot input files', infiles = '*', append = False, columns = 0, group = False, ordered = False)
    pp.parser.add_argument('-l', '--sourcelabels', nargs='+', help='labels for each source file in order')
    pp.parser.add_argument('-g', '--groups', nargs='+', help='columns in the sources that group')
    pp.parser.add_argument('-m', '--mapping', nargs='+', default='x=0 y=1', help='Mapping of columns in input files to plotting variables.' + \
        ' Can specify rows for multiple sources with the syntax var=0,1 where the column 0 refers to the first source and column 1 refers to the second source.' + \
        ' If a variable does not apply to all sources, you can skip them with var=,,1 to indicate that column 1 of the third source maps to the variable.' + \
        ' If only a single column is specified, it will be applied to all sources.' + \
        ' The variables available depend on the geom(s) chosen.' + \
        ' There is a special variable group that indicates grouping of input from a source into separate ')

    pp.parser.add_argument('-x', nargs='+', help='x-columns in the sources')
    pp.parser.add_argument('--xlabel', help='label for the x-axis')
    pp.parser.add_argument('--xrange', nargs=2, help='range for the x-axis')
    pp.parser.add_argument('--xtype', help='type of the x-axis')
    pp.parser.add_argument('--xformat', help='formatting for x values in source')
    pp.parser.add_argument('--xscale', default=['linear'], choices=['linear', 'log', 'asinh'])
    pp.parser.add_argument('--xmajorticks', nargs='+', help='positions of the major ticks')
    pp.parser.add_argument('--xmajorticklabels', nargs='+', help='custom labels for the major ticks')
    pp.parser.add_argument('--xminorticks', nargs='+', help='positions of the minor ticks')
    pp.parser.add_argument('--xtickformat', help='formatting for major x ticks')

    pp.parser.add_argument('-y', nargs='+', help='y-columns in the sources')
    pp.parser.add_argument('--ylabel', help='label for the y-axis')
    pp.parser.add_argument('--yrange', nargs=2, help='range for the y-axis')
    pp.parser.add_argument('--ytype', help='type for the y-axis')
    pp.parser.add_argument('--yformat', help='formatting for y values')
    pp.parser.add_argument('--yscale', default=['linear'], choices=['linear', 'log', 'asinh'])
    pp.parser.add_argument('--ymajorticks', nargs='+', help='positions of the major ticks')
    pp.parser.add_argument('--ymajorticklabels', nargs='+', help='custom labels for the major ticks')
    pp.parser.add_argument('--yminorticks', nargs='+', help='positions of the minor ticks')
    pp.parser.add_argument('--ytickformat', help='formatting for major y ticks')

    pp.parser.add_argument('-t', '--title')
    pp.parser.add_argument('--fontsize', type=int)
    pp.parser.add_argument('--geom', nargs='+')
    pp.parser.add_argument('--linetype', nargs='+')
    pp.parser.add_argument('--colour', nargs='+')
    pp.parser.add_argument('--shape', nargs='+')
    pp.parser.add_argument('--fill', nargs='+')
    pp.parser.add_argument('--alpha', nargs='+')
    pp.parser.add_argument('--size', nargs='+')
    pp.parser.add_argument('--canvas', nargs=2, type=float, help='Canvas width and height')
    pp.parser.add_argument('--filename', default='Pyplot.pdf')
    pp.parser.add_argument('--nolegend', action='store_true', default=False)
    pp.parser.add_argument('--legendposition', type=int)
    pp.parser.add_argument('--flip', action='store_true', default=False, help='flip x and y')
    args = pp.parseArgs()
    args = pp.getArgs(args)
    args.mapping = mappings(args)
    print args.mapping
    
    # Create the plot
    args.fig, args.ax = plt.subplots()
    if args.canvas:
        args.fig.set_size_inches(args.canvas[0], args.canvas[1])
    if args.title:
        args.ax.set_title(args.title)
    if args.xlabel:
        args.ax.set_xlabel(args.xlabel)
    if args.xrange:
        plt.xlim([fmt(args.xrange[0], args.xtype, args.xformat), fmt(args.xrange[1], args.xtype, args.xformat)])
    if args.ylabel:
        args.ax.set_ylabel(args.ylabel)
    if args.yrange:
        plt.ylim([fmt(args.yrange[0], args.ytype, args.yformat), fmt(args.yrange[1], args.ytype, args.yformat)])
    for i,infile in enumerate(args.infiles):
        
        run_grouping(infile, PlotGroup, args.group, False)

    if not args.nolegend:
        plt.legend(loc = args.legendposition if args.legendposition is not None else None)
    # Save plot
    plt.savefig('args.filename')
