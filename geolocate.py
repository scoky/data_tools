#!/usr/bin/python

import os
import sys
import maxminddb
import logging
import argparse
import traceback
from input_handling import findIPAddress

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Determine the country ISO code of domain name or IP address')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-g', '--geoip', default='geoip.mmdb', help='geoip database file to use')
    parser.add_argument('-c', '--column', type=int, default=0)
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

    jdelim = args.delimiter if args.delimiter != None else ' '
    rdr = maxminddb.Reader(args.geoip)
    for line in args.infile:
        try:
    	   chunk = line.split(args.delimiter)[args.column].rstrip()
	   try:
  	      ip = findIPAddress(chunk)
	      record = rdr.get(ip)
	      args.outfile.write(chunk+jdelim+record['country']['iso_code']+'\n')
	   except:
	      args.outfile.write(chunk+jdelim+'ERROR\n')
	except Exception as e:
           logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())

