#!/usr/bin/python

import os
import sys
import glob
import gzip
import logging
import argparse
import traceback
import parse_logs
from multiprocessing import Pool
from file_handle_dictionary import FileHandleDict

# Initializer and global variables for subprocesses
parser = None
parser_class = None
formatter = None
grouper = None
def initializer(prsr, frmtr, grp):
   global parser, formatter, grouper, parser_class
   parser = prsr()
   parser_class = prsr
   formatter = frmtr
   grouper = grp

def split_log(log):
   # Get a new parser instance for this file
   prsr = parser_class()
   fhd = FileHandleDict()

   logging.info('Splitting (file=%s) on (pid=%s)', log, os.getpid())
   try:
      with gzip.open(log, 'rb') if log.endswith('.gz') else open(log, 'r') as logf:
	 for line in logf:
	    result = prsr.parse(line)
	    output = formatter(result)
 	    group = log+grouper(result)

            if group not in fhd:
	       fhd[group] = open(group, 'a')
	    fhd[group].write(output)
   except Exception as e:
      logging.error('Error splitting log files: %s\n%s',\
         e, traceback.format_exc())
   finally:
      fhd.close_all()


def split_line(line):
   logging.info('Splitting line on (pid=%s)', log, os.getpid())
   result = parser.parse(line)
   output = formatter(result)
   group = grouper(result)
   return (output, group)

def main():
   logging.info('Command process (pid=%s)', os.getpid())

   parser_class = parse_logs.get_class(args.parser)

   formatter = eval(args.format)
   group = eval(args.group)
   pool = Pool(args.threads, initializer, (parser_class, formatter, group))
   fhd = FileHandleDict()
   try:
      if args.directory:  # Parsing 1 or more files
         args.logs = glob.glob(args.directory + '/*' + args.extension)
  	 results = pool.imap_unordered(split_log, args.logs, args.chunk)
	 for result in results:
	    pass
      else:		  # Parsing a single stream
	 results = pool.imap(split_line, args.infile, args.chunk)
	 for output, group in results:
            if group not in fhd:
	       fhd[group] = open(group, 'a')
	    fhd[group].write(output)
   except KeyboardInterrupt:
      sys.exit()
   finally:
      fhd.close_all()

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='General purpose log file parser')
    parser.add_argument('parser', default='default_parser.', type=str, help='line parser class to use')
    parser.add_argument('format', type=str, help='lambda that takes output of parser and returns output format')
    parser.add_argument('group', type=str, help='lambda that takes output of parser and returns string to split upon')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=str, default=None, help='preamble of output files')
    parser.add_argument('-d', '--directory', help='directory containing log files')
    parser.add_argument('-e', '--extension', default='', help='log file extension (for use with --directory option).')
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
