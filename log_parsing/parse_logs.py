#!/usr/bin/python

import os
import sys
import glob
import gzip
import logging
import argparse
import traceback
from multiprocessing import Pool

parser = None
parser_class = None
formatter = None
extension = None

class LineParser(object):
	def parse(self, line):
		raise NotImplementedError('This is an abstract method!')

def initializer(prsr, frmtr, xtnsn):
   global parser, formatter, extension, parser_class
   parser = prsr()
   parser_class = prsr
   formatter = frmtr
   extension = xtnsn

def parse_logs(log):
   # Get a new parser instance for this file
   prsr = parser_class()

   logging.info('Parsing (file=%s) on (pid=%s)', log, os.getpid())
   try:
      with gzip.open(log, 'rb') if log.endswith('.gz') else open(log, 'r') as logf:
	 with open(log+extension, 'w') as outf:
	    for line in logf:
	       result = prsr.parse(line)
	       outf.write(formatter(result)+'\n')
   except Exception as e:
      logging.error('Error splitting log files: %s\n%s',\
         e, traceback.format_exc())


def parse_lines(line):
   logging.info('Parsing line on (pid=%s)', log, os.getpid())
   result = parser.parse(line)
   output = formatter(result)+'\n'
   return output

def get_class(classname):
	# class is after the last dot
	mname, cname = classname.rsplit('.', 1)
	# import the module
	logging.info('Importing (class=%s) from (module=%s)', cname, mname)
	mod = __import__(mname, globals(), locals(), [cname], -1)
	# get the class
	cls = getattr(mod, cname)
	# make sure the class is a subclass of LineParser
#	assert(issubclass(cls, class(LineParser)))
	# return an instance of the class
	return cls

def main():
   logging.info('Command process (pid=%s)', os.getpid())

   parser_class = get_class(args.parser)

   formatter = eval(args.format)    
   pool = Pool(args.threads, initializer, (parser_class, formatter, args.output))
   try:
      if args.directory:  # Parsing 1 or more files
         args.logs = glob.glob(args.directory + '/*' + args.extension)
  	 results = pool.imap_unordered(parse_logs, args.logs, args.chunk)
	 for result in results:
	    pass
      else:		# Parsing a stream
	 results = pool.imap(parse_lines, args.infile, args.chunk)
	 for result in results:
	    args.outfile.write(result)
   except KeyboardInterrupt:
      sys.exit()

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='General purpose log file parser')
    parser.add_argument('parser', default='default_parser.', type=str, help='line parser class to use')
    parser.add_argument('format', type=str, help='format of output in lambda that takes output of parser')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-d', '--directory', help='directory containing log files')
    parser.add_argument('-e', '--extension', default='', help='log file extension (for use with --directory option).')
    parser.add_argument('-x', '--output', default='', help='output file extension (for use with --directory option).')
    parser.add_argument('-t', '--threads', default=None, type=int, help='number of threads to user')
    parser.add_argument('-c', '--chunk', default=20, help='chunk size to assign to each thread')
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
