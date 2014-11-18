#!/usr/bin/env python

import logging
import argparse
import sys
import traceback
import os
import socket
import time

BUFSIZE = 1024

def connect(address, port):
    before = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, port))
    after = time.time() - before
    print s.getsockname()[0], ':', s.getsockname()[1], ' -> ', address, ':', port, 'in', '%.3f' % after, 'seconds'
    return s

if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Connect to an address and wait.')
    parser.add_argument('address', default=None, help='ex: localhost:1234')
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

    sock = connect(args.address.split(':')[0], int(args.address.split(':')[1]))
    try:
	time.sleep(86400)
    except KeyboardInterrupt:
	sock.close()
        sys.exit()
