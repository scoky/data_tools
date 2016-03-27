#!/usr/bin/python

import os
import re
import sys
import glob
import string
import socket
import struct
import logging
import datetime
import argparse
import traceback
from copy import copy
from decimal import Decimal,InvalidOperation

number_pattern = re.compile("(-?\d+\.?\d*(e[\+|\-]?\d+)?)", re.IGNORECASE)
ip_pattern = re.compile("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")

def findIdentity(value):
    return value

def findFloat(value):
    return float(value)

def findInt(value):
    return int(value)

# Search an input value for a number
def findNumber(value):
    try:
        return Decimal(value)
    except InvalidOperation:
        return Decimal(number_pattern.search(value).group())

# Search an input value for a number
def findSignificantNumber(value, digits):
    try:
        return Decimal(value)
    except InvalidOperation:
        return Decimal(number_pattern.search(value).group())

def findIPAddress(value):
    try:
        # Might be a simple integer
        return int(value)
    except ValueError:
        m = ip_pattern.search(value)
        if m: # IP address in octet notation
	        return IPfromString(m.group())
        else: # Potentially a hostname
            return socket.gethostbyname(value)

def IPfromString(ip):
    return struct.unpack("!I", socket.inet_aton(ip))[0]

def IPtoString(ip):
    return socket.inet_ntoa(struct.pack("!I", int(ip)))

def MACfromString(mac):
    return int(mac.replace(':', ''), 16)

def MACtoString(mac):
    mac = hex(int(mac)).lstrip('0x')
    mac = '0'*(12-len(mac))+mac
    return ':'.join([mac[i:i+2] for i in xrange(0, len(mac), 2)])

def ToUnixTime(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.days*86400 + delta.seconds

def ToDateTime(dt):
    return datetime.datetime.utcfromtimestamp(dt)

def parseLines(infile, delimiter=None, columns=[0], function=findIdentity):
    for line in infile:
        try:
            chunks = line.rstrip().split(delimiter)
            yield [function(chunks[i]) for i in columns]
        except IndexError as e:
            logging.error('Error on input: %s%s\n%s', line, e, traceback.format_exc())

def concatFiles(files, opts='r'):
    for f in files:
        for line in openFile(f, opts):
            yield line

def fileRange(startFile, endFile):
    startDir, startFile = os.path.split(startFile)
    _, endFile = os.path.split(endFile)
    if startDir == '':
        files = glob.iglob('*');
    else:
        files = glob.iglob(os.path.expanduser(startDir) + '/*');
    ret = []
    for fn in files:
        if startFile <= os.path.basename(fn) <= endFile:
            ret.append(fn)
    return sorted(ret)

def openFile(filename, opts):
    return gzip.open(filename, opts+'b') if filename.endswith('.gz') else open(filename, opts)

class Header:
    def __init__(self, columns = [], exists = True):
        self.columns = columns
        self.exists = exists
        
    def __len__(self):
        return len(self.columns)

    def __iter__(self):
        return self.columns.__iter__()
        
    def setCol(self, colName, index):
        while len(self.columns) <= index:
            self.columns.append(str(len(self.columns)))
        self.columns[index] = colName
        
    def addCol(self, colName):
        col = colName
        i = 1
        while col in self.columns:
            col = colName+str(i)
            i += 1
        self.columns.append(col)
        return len(self.columns) - 1

    def addCols(self, colNames):
        return [self.addCol(colName) for colName in colNames]
        
    def extend(self, header):
        self.addCols(header.columns)

    def value(self, delimiter):
        if self.exists:
            return delimiter.join(self.columns)+'\n'
        else:
            return ''

    def index(self, colName):
        if colName is None:
            return colName
        elif colName in self.columns:
            return self.columns.index(colName)
        else:
            try:
                return int(colName)
            except ValueError as e:
                raise ValueError('Invalid column specified', e)

    def indexes(self, colNames):
        return [self.index(colName) for colName in colNames]

    def name(self, index):
        try:
            return self.columns[int(index)]
        except ValueError:
            return 'col_'+str(index)
        except IndexError:
            return 'col_'+str(index)

    def names(self, indexes):
        return [self.name(index) for index in indexes]

    def copy(self):
        return Header(copy(self.columns), self.exists)

class FileReader:
    def __init__(self, inputStream, header = False, delimiter = None):
        if type(inputStream) == str:
            self.inputStream = openFile(inputStream, 'r')
        elif type(inputStream) == file:
            self.inputStream = inputStream
        else:
            raise IOError('Unknown input stream type: %s' % type(inputStream))

        self.delimiter = delimiter if delimiter else os.environ.get('TOOLBOX_DELIMITER', ' ')
        header = header or os.environ.get('TOOLBOX_HEADER', '').lower() == 'true'
        if header:
            self.header = self._readHeader()
        else:
            self.header = Header([], exists = False)

    def Delimiter(self):
        return self.delimiter

    def Header(self):
        return self.header

    def _readHeader(self):
        preamble = self.inputStream.next()
        return Header(preamble.strip().split(self.delimiter))
        
    def __iter__(self):
        return self
        
    def next(self):
        return self.inputStream.next().strip().split(self.delimiter)

    def readline(self):
        try:
            return self.next()
        except StopIteration:
            return ''

    def close(self):
        self.inputStream.close()

    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Parse input base upon available functions')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-c', '--columns', nargs='+', type=int, default=[0])
    parser.add_argument('-a', '--append', action='store_true', default=False, help='append result to columns')
    parser.add_argument('-f', '--function', choices=['IPtoString', 'IPfromString', 'MACtoString', 'MACfromString', 'findNumber', 'findIPAddress'], default='findNumber')
    parser.add_argument('-d', '--delimiter', default=None)
    args = parser.parse_args()
    args.function = getattr(sys.modules[__name__], args.function)

    jdelim = args.delimiter if args.delimiter != None else ' '
    for line in args.infile:
        chunks = line.rstrip().split(args.delimiter)
        vals = [args.function(chunks[i]) for i in args.columns]
        if args.append:
            args.outfile.write('%s%s' % (line.rstrip(), jdelim))
        args.outfile.write(jdelim.join(map(str,vals))+'\n')
    
