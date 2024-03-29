#!/usr/bin/env python

import os,sys,argparse
from data_tools.files import ParameterParser
from data_tools.group import Group,run_grouping

header='''<html>
  <head>
    <script type='text/javascript' src='https://www.gstatic.com/charts/loader.js'></script>
    <script type='text/javascript'>
     google.charts.load('upcoming', {'packages': ['geochart']});
     google.charts.setOnLoadCallback(drawMarkersMap);
    function drawMarkersMap() {
      var data = google.visualization.arrayToDataTable(['''

footer=''']);
      var options = {{
        sizeAxis: {{ minSize: {minSize}, maxSize: {maxSize} }},
        region: '{map}',
        displayMode: '{mode}',
        legend: 'none',
        tooltip: {{ showColorCode: false, trigger: '{trigger}' }},
        colorAxis: {{ minValue: {minValue}, maxValue: {maxValue}, colors: ['{minColor}', '{maxColor}'] }}
      }};
      var chart = new google.visualization.GeoChart(document.getElementById('chart_div'));
      chart.draw(data, options);
    }};
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: {width}px; height: {height}px;"></div>
  </body>
</html>'''

class MapGroup(Group):
    def __init__(self, tup):
        super(MapGroup, self).__init__(tup)

    def add(self, chunks):
        chunks = [chunks[i] for i in args.columns]
        for i,chunk in enumerate(chunks):
          try:
            float(chunks[i])
          except ValueError:
            chunks[i] = "'{0}'".format(chunks[i])
        print("[{0}],".format(", ".join(chunks)))

    def done(self):
        pass

if __name__ == "__main__":
    pp = ParameterParser('Plot maps of input files', infiles = '*', append = False, columns = '*', labels = [None], group = False, ordered = False)
    pp.parser.add_argument('-m', '--map', default='world', help='map to plot upon')
    pp.parser.add_argument('--size', default=[5, 5], nargs=2, type=int, help='size range of the markers')
    pp.parser.add_argument('--mode', default='auto', choices=['auto', 'markers', 'regions', 'text'])
    pp.parser.add_argument('--trigger', default='focus', choices=['none', 'focus', 'selection'], help='trigger for displaying tooltips')
    pp.parser.add_argument('--color-codes', default=[0, 1], nargs=2, type=int, help='range of values in color input')
    pp.parser.add_argument('--color-range', default=['#FF0000', '#00FF00'], nargs=2, help='range of colors to display')
    pp.parser.add_argument('--canvas', nargs=2, type=int, default=[500,300], help='canvas width and height in pixels')
    args = pp.parseArgs()
    if not any(args.labels):
        args.labels = args.columns_names
    args = pp.getArgs(args)
    print(header)
    print("['{0}'],".format("', '".join(args.labels)))
    for i,infile in enumerate(args.infiles):
        run_grouping(infile, MapGroup, [], False)
        infile.close()
    print(footer.format(minSize=min(args.size),
                        maxSize=max(args.size),
                        map=args.map,
                        mode=args.mode,
                        trigger=args.trigger,
                        minValue=min(args.color_codes),
                        maxValue=max(args.color_codes),
                        minColor=min(args.color_range),
                        maxColor=max(args.color_range),
                        width=args.canvas[0],
                        height=args.canvas[1]))
