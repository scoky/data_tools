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
from matplotlib.ticker import FormatStrFormatter
from matplotlib.dates import DateFormatter
from matplotlib.artist import setp

class PlotGroup(Group):
    def __init__(self, tup):
        super(PlotGroup, self).__init__(tup)
        self.data = {}
        for v in args.current.mapping:
            self.data[v] = []
        # if 'y' not in self.data or 'x' not in self.data:
        #     raise ValueError('Missing required mapping x or y')

    def add(self, chunks):
        for v,c in args.current.mapping.iteritems():
            self.data[v].append(chunks[c])

    def done(self):
        for geom in args.current.geom.split('+'):
            if not hasattr(self, 'plot_{0}'.format(geom)):
                raise ValueError('Invalid geometry {0} specified'.format(geom))
            obj = getattr(self, 'plot_{0}'.format(geom))()

            if args.current.label and len(self.tup) > 0:
                label = "{0}: {1}".format(args.current.label if args.current.label else '', ' '.join(self.tup))
                obj.set_label(label)
            elif args.current.label:
                #obj.set_label(args.current.label)
                pass
            elif len(self.tup) > 0:
                obj.set_label(' '.join(self.tup))

    def plot_line(self):
        line, = args.ax.plot([fmt(x, args.xtype, args.xformat) for x in self.data['x']],
            [fmt(y, args.ytype, args.yformat) for y in self.data['y']],
            args.current.shape if args.current.shape else '-')
        if args.current.colour:
            line.set_color(args.current.colour)
        if args.current.size:
            setp(line, linewidth=args.current.size)
            line.set_markersize(args.current.size)
        if args.current.alpha:
            line.set_alpha(args.current.alpha)
        return line

    def plot_errorbar(self):
        err = None
        if 'ylow' in self.data and 'yhigh' in self.data:
            err = [[fmt(y, args.ytype, args.yformat) for y in self.data['ylow']], [fmt(y, args.ytype, args.yformat) for y in self.data['yhigh']]]
        elif 'ydelta' in self.data:
            err = [fmt(y, args.ytype, args.yformat) for y in self.data['ydelta']]
        else:
            raise ValueError('Missing mapping for ylow and yhigh or ydelta')
        line = args.ax.errorbar([fmt(x, args.xtype, args.xformat) for x in self.data['x']],
            [fmt(y, args.ytype, args.yformat) for y in self.data['y']],
            yerr = err, fmt = args.current.shape if args.current.shape else 'o')
        if args.current.colour:
            line.set_color(args.current.colour)
        if args.current.size:
            setp(line, linewidth=args.current.size)
            #line.set_markersize(args.current.size)
            #setp(line, elinewidth=args.current.size)
        return line

    def plot_bar(self):
        if not hasattr(args, 'baroffset'):
            args.baroffset = 0
        bars = args.ax.bar([fmt(x, args.xtype, args.xformat) + args.baroffset for x in self.data['x']],
            [fmt(y, args.ytype, args.yformat) for y in self.data['y']])

        for bar in bars:
            if args.current.colour:
                bar.set_color(args.current.colour)
            if args.current.size:
                setp(bar, width=args.current.size)
            if args.current.alpha:
                bar.set_alpha(args.current.alpha)
        args.baroffset += bars[0].get_width()
        return bars

    def plot_stackbar(self):
        y = np.array([fmt(y, args.ytype, args.yformat) for y in self.data['y']])
        bars = args.ax.bar([fmt(x, args.xtype, args.xformat) for x in self.data['x']],
            y,
            bottom = args.stackbottom if hasattr(args, 'stackbottom') else None)
        # Save the bottom position for next data
        if hasattr(args, 'stackbottom'):
            args.stackbottom += y
        else:
            args.stackbottom = y

        for bar in bars:
            if args.current.colour:
                bar.set_color(args.current.colour)
            if args.current.size:
                setp(bar, width=args.current.size)
            if args.current.alpha:
                bar.set_alpha(args.current.alpha)
        return bars

    def plot_point(self):
        if not args.current.shape:
            args.current.shape = 'o'
        return self.plot_line() # Lines and points are the same in matplotlib, shape is the only difference

    def plot_step(self):
        line = self.plot_line()
        line.set_drawstyle('steps')
        return line

    def plot_boxplot(self):
        if not hasattr(args, 'boxplotx'):
            args.boxplotx = 1
        box = args.ax.boxplot([fmt(y, args.ytype, args.yformat) for y in self.data['sample']],
            positions=[args.boxplotx])
        args.boxplotx += 1
        return box

    def plot_ribbon(self):
        if 'yy' not in self.data:
            raise ValueError('Missing mapping for yy')
        ribbon = args.ax.fill_between([fmt(x, args.xtype, args.xformat) for x in self.data['x']],
            [fmt(y, args.ytype, args.yformat) for y in self.data['y']],
            [fmt(y, args.ytype, args.yformat) for y in self.data['yy']])
        if args.current.colour:
            ribbon.set_color(args.current.colour)
        if args.current.alpha:
            ribbon.set_alpha(args.current.alpha)
        return ribbon

class Source(object):
    def __init__(self, infile):
        self.infile = infile

def mappings(args):
    try:
        parts = (' '.join(args.mapping)).split('=')
        maps = {}

        v = parts[0].strip()
        for part in parts[1:-1]:
            m, v_next = part.rsplit(None, 1)
            maps[v] = [None if m1.strip() == '' else m1.strip() for m1 in m.split(',')]
            if len(maps[v]) == 1:
                maps[v] = maps[v] * len(args.infiles)
            elif len(maps[v]) != len(args.infiles):
                raise ValueError('Wrong number of mappings specified for variable {0}'.format(v))
            v = v_next.strip()
        maps[v] = [None if m1.strip() == '' else m1.strip() for m1 in parts[-1].split(',')]
        if len(maps[v]) == 1:
            maps[v] = maps[v] * len(args.infiles)
        elif len(maps[v]) != len(args.infiles):
            raise ValueError('Wrong number of mappings specified for variable {0}'.format(v))
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

def tick_fmt(vtype, vformat):
    if vtype == 'int' or vtype == 'float':
        return FormatStrFormatter(vformat)
    elif vtype == 'datetime':
        return DateFormatter(vformat)

if __name__ == "__main__":
    pp = ParameterParser('Plot input files', infiles = '*', append = False, columns = 0, group = False, ordered = False)
    pp.parser.add_argument('-l', '--sourcelabels', nargs='+', help='labels for each source file in order')
    pp.parser.add_argument('-g', '--groups', nargs='+', help='columns in the sources that group (not implemented!)')
    pp.parser.add_argument('-m', '--mapping', nargs='+', default='x=0 y=1', help='Mapping of columns in input files to plotting variables.' + \
        ' Can specify rows for multiple sources with the syntax var=0,1 where the column 0 refers to the first source and column 1 refers to the second source.' + \
        ' If a variable does not apply to all sources, you can skip them with var=,,1 to indicate that column 1 of the third source maps to the variable.' + \
        ' If only a single column is specified, it will be applied to all sources.' + \
        ' The variables available depend on the geom(s) chosen.' + \
        ' There is a special variable group that indicates grouping of input from a source into separate ')

    pp.parser.add_argument('-x', '--xlabel', help='label for the x-axis')
    pp.parser.add_argument('--xrange', nargs=2, help='range for the x-axis')
    pp.parser.add_argument('--xtype', help='type of the x-axis', default='float', choices=['int', 'float', 'datetime'])
    pp.parser.add_argument('--xformat', help='formatting for x values in source')
    pp.parser.add_argument('--xscale', choices=['linear', 'log', 'logit', 'symlog'])
    pp.parser.add_argument('--xmajorticks', nargs='+', help='positions of the major ticks')
    pp.parser.add_argument('--xmajorticklabels', nargs='+', help='custom labels for the major ticks')
    pp.parser.add_argument('--xminorticks', nargs='+', help='positions of the minor ticks')
    pp.parser.add_argument('--xtickformat', help='formatting for major x ticks')

    pp.parser.add_argument('-y', '--ylabel', help='label for the y-axis')
    pp.parser.add_argument('--yrange', nargs=2, help='range for the y-axis')
    pp.parser.add_argument('--ytype', help='type for the y-axis', default='float', choices=['int', 'float', 'datetime'])
    pp.parser.add_argument('--yformat', help='formatting for y values')
    pp.parser.add_argument('--yscale', default='linear', choices=['linear', 'log', 'logit', 'symlog'])
    pp.parser.add_argument('--ymajorticks', nargs='+', help='positions of the major ticks')
    pp.parser.add_argument('--ymajorticklabels', nargs='+', help='custom labels for the major ticks')
    pp.parser.add_argument('--yminorticks', nargs='+', help='positions of the minor ticks')
    pp.parser.add_argument('--ytickformat', help='formatting for major y ticks')

    pp.parser.add_argument('-t', '--title')
    pp.parser.add_argument('--fontsize', type=int)
    pp.parser.add_argument('--geom', default=['line'], nargs='+', help='How to plot the sources.' + \
        ' Supported geometries with mappings include:' + \
        ' line => x, y;' + \
        ' errorbar => x, y, ydelta or ylow, yhigh;' + \
        ' bar => x, y;' + \
        ' stackbar => x, y;' + \
        ' point => x, y;' + \
        ' step => x, y;' + \
        ' boxplot => sample;' + \
        ' ribbon => x, y, yy.')
    pp.parser.add_argument('--colour', nargs='+')
    pp.parser.add_argument('--shape', nargs='+')
    pp.parser.add_argument('--fill', nargs='+')
    pp.parser.add_argument('--alpha', nargs='+', type=float)
    pp.parser.add_argument('--size', nargs='+', type=float)
    pp.parser.add_argument('--canvas', nargs=2, type=float, help='Canvas width and height')
    pp.parser.add_argument('--filename', default='Pyplot.pdf')
    pp.parser.add_argument('--nolegend', action='store_true', default=False)
    pp.parser.add_argument('--legendposition', type=int)
    pp.parser.add_argument('--flip', action='store_true', default=False, help='flip x and y (not implemented!)')
    args = pp.parseArgs()
    args = pp.getArgs(args)
    # Validate inputs
    for attr in ['geom', 'sourcelabels', 'colour', 'shape', 'fill', 'alpha', 'size']:
        if getattr(args, attr) is None:
            setattr(args, attr, [None] * len(args.infiles))
        elif len(getattr(args, attr)) == 1:
            setattr(args, attr, getattr(args, attr) * len(args.infiles))
        elif len(getattr(args, attr)) != len(args.infiles):
            raise ValueError('Wrong number of mappings specified for {0}'.format(attr))
    args.mapping = mappings(args)

    # Create the plot
    args.fig, args.ax = plt.subplots()
    if args.fontsize:
        matplotlib.rcParams.update({'font.size': args.fontsize})
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
    if args.xtype == 'datetime':
        args.fig.autofmt_xdate()
    if args.ytype == 'datetime':
        args.fig.autofmt_xdate()

    # Process sources in order
    for i,infile in enumerate(args.infiles):
        s = Source(infile)
        s.mapping = {v : infile.header.index(args.mapping[v][i]) for v in args.mapping if args.mapping[v][i] is not None}
        s.geom = args.geom[i]
        s.label = args.sourcelabels[i]
        s.colour = args.colour[i]
        s.shape = args.shape[i]
        s.fill = args.fill[i]
        s.alpha = args.alpha[i]
        s.size = args.size[i]
        args.current = s
        run_grouping(infile, PlotGroup, [], False)

    if args.xscale:
        args.ax.set_xscale(args.xscale)
    if args.xmajorticks:
        args.ax.set_xticks([fmt(x, args.xtype, args.xformat) for x in args.xmajorticks])
        if args.xmajorticklabels:
            args.ax.set_xticklabels(args.xmajorticklabels)
    if args.xminorticks:
        args.ax.set_xticks([fmt(x, args.xtype, args.xformat) for x in args.xminorticks], minor = True)
    if args.xtickformat:
        args.ax.xaxis.set_major_formatter(tick_fmt(args.xtype, args.xtickformat))

    if args.yscale:
        args.ax.set_yscale(args.yscale)
    if args.ymajorticks:
        args.ax.set_yticks([fmt(y, args.ytype, args.yformat) for y in args.ymajorticks])
        if args.ymajorticklabels:
            args.ax.set_yticklabels(args.ymajorticklabels)
    if args.yminorticks:
        args.ax.set_yticks([fmt(y, args.ytype, args.yformat) for y in args.yminorticks], minor = True)
    if args.ytickformat:
        args.ax.yaxis.set_major_formatter(tick_fmt(args.ytype, args.ytickformat))

    if not args.nolegend:
        plt.legend(loc = args.legendposition if args.legendposition is not None else None)
    # Save plot
    plt.savefig(args.filename)
