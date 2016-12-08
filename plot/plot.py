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
from matplotlib.pyplot import cm
from itertools import izip
from datetime import datetime

def ColMaps(req = [], opt = []):
  def hook(fn):
    fn.required_mappings = req
    fn.optional_mappings = opt
    return fn
  return hook

class LoopIterator(object):
  def __init__(self, items, shift = 1):
    self.items = items
    self.shift = shift
    self.i = 0 - self.shift
    self._enable = True
  def reset(self):
    self.i = -1
  def enable(self):
    self._enable = True
  def __iter__(self):
    return self
  def next(self):
    if self._enable:
      self.i = (self.i + self.shift) % len(self.items)
      self._enable = False
    return self.items[self.i]

class LineStyles(LoopIterator):
  def __init__(self, styles = ['-', '--', '-.', ':']):
    super(LineStyles, self).__init__(items = styles)

class MarkerStyles(LoopIterator):
  def __init__(self, styles = ['o', 's', 'd', 'D', '>', '<', '^', 'v']):
    super(MarkerStyles, self).__init__(items = styles)

class Colours(LoopIterator):
  def __init__(self, palette = 'rainbow', count = 15, shift = 4):
    super(Colours, self).__init__(items = getattr(cm, palette)(np.linspace(0, 1, count)), shift = shift)

class PlotGroup(Group):
    def __init__(self, tup):
        super(PlotGroup, self).__init__(tup)
        self.data = {}
        for v in args.current.mapping:
            self.data[v] = []

    def add(self, chunks):
        for v,c in args.current.mapping.iteritems():
            self.data[v].append(chunks[c])

    def done(self):
        label = ''
        if args.sourcelabels:
          args.sourcelabels.enable()
          label = args.sourcelabels.next()
          if len(self.tup) > 0:
            label = "{0}: {1}".format(label, ' '.join(self.tup))
        elif len(self.tup) > 0:
            label = ' '.join(self.tup)

        # Allow advancement
        if args.colours:
          args.colours.enable()
        if args.alpha:
          args.alpha.enable()
        if args.size:
          args.size.enable()
        if args.lines:
          args.lines.enable()
        if args.markers:
          args.markers.enable()
        if args.fill:
          args.fill.enable()

        args.geom.enable()
        for geom in args.geom.next().split('+'):
            if not hasattr(self, 'plot_{0}'.format(geom)):
                raise ValueError('Invalid geometry {0} specified'.format(geom))
            f = getattr(self, 'plot_{0}'.format(geom))

            # Generate default appearance
            kwargs = { 'label' : label }
            if args.colours is not None:
                kwargs['color'] = args.colours.next()
            if args.alpha is not None:
                kwargs['alpha'] = args.alpha.next()

            # Make sure all required mappings are present
            for m in getattr(f, 'required_mappings'):
                if m not in self.data:
                    raise ValueError('Missing required mapping {0}'.format(m))
            # Add the optional mappings to the dictionary
            for m in getattr(f, 'optional_mappings'):
                if m in self.data:
                    kwargs[m] = self.data[m]
            f(kwargs)
            args.plotted_items += 1

    @ColMaps(req = ['x', 'y'])
    def plot_line(self, kwargs):
        # For lines, size sets both linewidth and markersize
        if args.size:
            if 'linewidth' not in kwargs:
                kwargs['linewidth'] = args.size.next()
            if 'markersize' not in kwargs:
                kwargs['markersize'] = args.size.next()
        if args.lines:
          kwargs['linestyle'] = args.lines.next()
        if args.markers:
          kwargs['marker'] = args.markers.next()

        # Draw line
        line = args.ax.plot([fmt(x, args.xtype, args.xformat) for x in self.data['x']],
            [fmt(y, args.ytype, args.yformat) for y in self.data['y']],
            **kwargs)

        return line

    @ColMaps(req = ['x', 'y'], opt = ['yhigh', 'ylow', 'ydelta'])
    def plot_errorbar(self, kwargs):
        err = None
        if 'ylow' in self.data and 'yhigh' in self.data:
            err = [[fmt(y, args.ytype, args.yformat) for y in self.data['ylow']], [fmt(y, args.ytype, args.yformat) for y in self.data['yhigh']]]
            del kwargs['ylow']
            del kwargs['yhigh']
        elif 'ydelta' in self.data:
            err = [fmt(y, args.ytype, args.yformat) for y in self.data['ydelta']]
            del kwargs['ydelta']
        else:
            err = []

        if args.size:
            s = args.size.next()
            if 'linewidth' not in kwargs:
                kwargs['linewidth'] = s
            if 'elinewidth' not in kwargs:
                kwargs['elinewidth'] = s
            if 'markeredgewidth' not in kwargs:
                kwargs['markeredgewidth'] = s
            if 'markersize' not in kwargs:
                kwargs['markersize'] = s
        if args.lines:
          kwargs['linestyle'] = args.lines.next()
        if args.markers:
          kwargs['marker'] = args.markers.next()

        # Draw error bars
        bars = args.ax.errorbar([fmt(x, args.xtype, args.xformat) for x in self.data['x']],
            [fmt(y, args.ytype, args.yformat) for y in self.data['y']],
            yerr = err,
            **kwargs)

        return bars

    @ColMaps(req = ['x', 'y'])
    def plot_bar(self, kwargs):
        bars = self.plot_stackbar(kwargs)
        args.baroffset += bars[0].get_width()
        args.stackbottom = {}

        return bars

    @ColMaps(req = ['x', 'y'])
    def plot_stackbar(self, kwargs):
        if args.size:
            kwargs['width'] = args.size.next()

        # Draw bars
        if not hasattr(args, 'baroffset'):
            args.baroffset = 0
        if not hasattr(args, 'stackbottom'):
            args.stackbottom = {}

        bottom = []
        y = np.array([fmt(y, args.ytype, args.yformat) for y in self.data['y']])
        x = np.array([fmt(x, args.xtype, args.xformat) + args.baroffset for x in self.data['x']])
        # Set the bottom position for this data and save the bottom position for the next
        for xx,yy in izip(x,y):
          if xx in args.stackbottom:
            bottom.append(args.stackbottom[xx])
            args.stackbottom[xx] += yy
          else:
            bottom.append(fmt(None, args.ytype, args.yformat))
            args.stackbottom[xx] = yy

        bars = args.ax.bar(x, y,
            bottom = bottom,
            **kwargs)

        return bars

    @ColMaps(req = ['x', 'y'])
    def plot_point(self, kwargs):
        if args.size:
            kwargs['s'] = args.size.next()
        if args.markers:
            kwargs['marker'] = args.markers.next()

        # Draw points
        line = args.ax.scatter([fmt(x, args.xtype, args.xformat) for x in self.data['x']],
            [fmt(y, args.ytype, args.yformat) for y in self.data['y']],
            **kwargs)

        return line

    @ColMaps(req = ['x', 'y'])
    def plot_step(self, kwargs):
        line = self.plot_line(kwargs)
        for l in line:
            l.set_drawstyle('steps')
        return line

    @ColMaps(req = ['sample'])
    def plot_boxplot(self, kwargs):
        if not hasattr(args, 'boxplotx'):
            args.boxplotx = 1
        box = args.ax.boxplot([fmt(y, args.ytype, args.yformat) for y in self.data['sample']],
            positions=[args.boxplotx],
            **kwargs)
        args.boxplotx += 1
        return box

    @ColMaps(req = ['x', 'y'], opt = ['yy'])
    def plot_ribbon(self, kwargs):
        y = [fmt(yi, args.ytype, args.yformat) for yi in self.data['y']]
        if 'yy' in self.data:
            yy = [fmt(yi, args.ytype, args.yformat) for yi in self.data['yy']]
            del kwargs['yy']
        else:
            yy = [0]*len(y)

        ribbon = args.ax.fill_between([fmt(x, args.xtype, args.xformat) for x in self.data['x']],
            y, yy,
            **kwargs)
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
          if value is None:
            return 0
          else:
            return int(value)
        elif vtype == 'float':
          if value is None:
            return 0.0
          else:
            return float(value)
        elif vtype == 'datetime':
          if value is None:
            return datetime.min
          else:
            return datetime.strptime(value, vformat)
    except Exception as e:
        raise ValueError('Input value error ({0} {1} {2})'.format(value, vtype, vformat), e)

def tick_fmt(vtype, vformat):
    if vtype == 'int' or vtype == 'float':
        return FormatStrFormatter(vformat)
    elif vtype == 'datetime':
        return DateFormatter(vformat)

if __name__ == "__main__":
    pp = ParameterParser('Plot input files', infiles = '*', append = False, columns = 0, group = True, ordered = False)
    pp.parser.add_argument('-l', '--sourcelabels', nargs='+', help='labels for each source file in order')
    pp.parser.add_argument('-m', '--mapping', nargs='+', default='x=0 y=1', help='Mapping of columns in input files to plotting variables.' + \
        ' Can specify rows for multiple sources with the syntax var=0,1 where the column 0 refers to the first source and column 1 refers to the second source.' + \
        ' If a variable does not apply to all sources, you can skip them with var=,,1 to indicate that column 1 of the third source maps to the variable.' + \
        ' If only a single column is specified, it will be applied to all sources.' + \
        ' The variables available depend on the geom(s) chosen.')

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
        ' Use --geom help to display supported geometries and their mappings.')
    pp.parser.add_argument('--colours', nargs='+', help='colors to rotate through')
    pp.parser.add_argument('--colourmap', default='rainbow', help='rotate through the map. overridden by --colour')
    pp.parser.add_argument('--lines', nargs='+', help='auto')
    pp.parser.add_argument('--markers', nargs='+', help='auto')
    pp.parser.add_argument('--fill', nargs='+', help='auto')
    pp.parser.add_argument('--alpha', nargs='+', type=float)
    pp.parser.add_argument('--size', nargs='+', type=float)
    pp.parser.add_argument('--canvas', nargs=2, type=float, help='Canvas width and height')
    pp.parser.add_argument('--filename', default='Pyplot.pdf')
    pp.parser.add_argument('--nolegend', action='store_true', default=False)
    pp.parser.add_argument('--legendposition', type=int)
    pp.parser.add_argument('--legendfontsize')
    pp.parser.add_argument('--flip', action='store_true', default=False, help='flip x and y (not implemented!)')
    args = pp.parseArgs()
    args = pp.getArgs(args)
    if args.colours is None:
      args.colours = Colours(args.colourmap)
    else:
      args.colours = LoopIterator(args.colours)
    if args.markers is not None and len(args.markers) == 1 and args.markers[0] == 'auto':
      args.markers = MarkerStyles()
    elif args.markers is not None:
      args.markers = LoopIterator(args.markers)
    if args.lines is not None and len(args.lines) == 1 and args.lines[0] == 'auto':
      args.lines = LineStyles()
    elif args.lines is not None:
      args.lines = LoopIterator(args.lines)
    if args.fill is not None and len(args.fill) == 1 and args.fill[0] == 'auto':
      args.fill = Colours(args.colourmap)
    elif args.fill is not None:
      args.fill = LoopIterator(args.fill)
    if args.alpha is not None:
      args.alpha = LoopIterator(args.alpha)
    if args.size is not None:
      args.size = LoopIterator(args.size)
    if args.sourcelabels is not None:
      args.sourcelabels = LoopIterator(args.sourcelabels)

    args.plotted_items = 0
    # Print help information about available geoms
    if args.geom[0].lower() == 'help':
        import inspect
        for method_name,method in inspect.getmembers(PlotGroup, predicate = inspect.ismethod):
            if method_name.startswith('plot_'):
                geom = method_name.split('_', 1)[1]
                opt = ''
                if len(method.optional_mappings) > 0:
                    opt = 'opt => {0}'.format(', '.join(method.optional_mappings))
                print geom, ': req =>', ', '.join(method.required_mappings), opt
        sys.exit()
    args.geom = LoopIterator(args.geom)

    # Validate inputs
    # for attr in ['geom', 'sourcelabels', 'colour', 'shape', 'fill', 'alpha', 'size']:
    #     if getattr(args, attr) is None:
    #         setattr(args, attr, [None] * len(args.infiles))
    #     elif len(getattr(args, attr)) == 1:
    #         setattr(args, attr, getattr(args, attr) * len(args.infiles))
    #     elif len(getattr(args, attr)) != len(args.infiles):
    #         raise ValueError('Wrong number of mappings specified for {0}'.format(attr))
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
        args.fig.autofmt_ydate()
    # if args.colourmap is not None:
    #     args.ax.set_color_cycle(plt.get_cmap(args.colourmap[0])(np.linspace(0,1,int(args.colourmap[1]))))

    # Process sources in order
    for i,infile in enumerate(args.infiles):
        s = Source(infile)
        s.mapping = {v : infile.header.index(args.mapping[v][i]) for v in args.mapping if args.mapping[v][i] is not None}
        # s.geom = args.geom[i]
        # s.label = args.sourcelabels[i]
        # s.colour = args.colour[i]
        # s.shape = args.shape[i]
        # s.fill = args.fill[i]
        # s.alpha = args.alpha[i]
        # s.size = args.size[i]
        args.current = s
        run_grouping(infile, PlotGroup, args.group, False)
        infile.close()

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
        args.ax.set_yscale(args.yscale, nonposy='clip')
    if args.ymajorticks:
        args.ax.set_yticks([fmt(y, args.ytype, args.yformat) for y in args.ymajorticks])
        if args.ymajorticklabels:
            args.ax.set_yticklabels(args.ymajorticklabels)
    if args.yminorticks:
        args.ax.set_yticks([fmt(y, args.ytype, args.yformat) for y in args.yminorticks], minor = True)
    if args.ytickformat:
        args.ax.yaxis.set_major_formatter(tick_fmt(args.ytype, args.ytickformat))

    if not args.nolegend:
        plt.legend(loc = args.legendposition if args.legendposition is not None else 0, fontsize = args.legendfontsize)
    # Save plot
    plt.savefig(args.filename)
