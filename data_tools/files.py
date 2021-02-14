#!/usr/bin/env python

import os
import re
import sys
import glob
import argparse
from copy import copy
from decimal import Decimal,InvalidOperation

number_pattern = re.compile("(-?\d+\.?\d*(e[\+|\-]?\d+)?)", re.IGNORECASE)

# Search an input value for a number
def findNumber(value):
    try:
        return Decimal(value)
    except InvalidOperation:
        try:
            return Decimal(number_pattern.search(value.replace(',', '')).group())
        except AttributeError:
            raise Exception('Value "{0}" does not contain a number'.format(value))

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
    if type(filename) is str:
        if filename == '-':
            return sys.stdin if opts == 'r' else sys.stdout
        else:
            return gzip.open(os.path.expanduser(filename), opts+'b') if filename.endswith('.gz') else open(os.path.expanduser(filename), opts)
    elif type(filename) is file:
        return filename
    else:
        raise IOError('Unknown input type: %s' % type(filename))

class Header:
    def __init__(self, columns = []):
        self.columns = columns
        
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

    def index(self, colName):
        if colName is None:
            return colName
        elif colName in self.columns:
            return self.columns.index(colName)
        else:
            try:
                return int(colName)
            except ValueError as e:
                raise ValueError('Invalid column %s specified' % colName)

    def indexes(self, colNames):
        return [self.index(colName) for colName in colNames]

    def name(self, index):
        try:
            return self.columns[int(index)]
        except ValueError:
            return str(index)
        except IndexError:
            return 'col_'+str(index)

    def names(self, indexes):
        return [self.name(index) for index in indexes]

    def copy(self):
        return Header(copy(self.columns))

class FileWriter:
    def __init__(self, outputStream, reader, args, opts = 'w'):
        self._outputStream = openFile(outputStream, opts)
        self._delimiter = args.delimiter if args.delimiter else os.environ.get('TOOLBOX_DELIMITER', ' ')
        self.write = self._firstwrite
        self._header = Header()
        if reader and reader.hasHeader:
            if hasattr(args, 'append') and args.append:
                self._header = reader.header.copy()
            else:
                if hasattr(args, 'group'):
                    self._header.addCols(reader.header.names(args.group))
            if hasattr(args, 'labels'):
                self._header.addCols(args.labels)

    @property
    def header(self):
        return self._header

    @property
    def hasHeader(self):
        return len(self._header.columns) > 0

    def _firstwrite(self, chunks):
        self.write = self._write
        if self.hasHeader:
            self.write(self._header.columns)
            if len(self._header) != len(chunks):
                sys.stderr.write('Warning: number of rows in output does not match number of rows in header\n')
        self.write(chunks)

    def _write(self, chunks):
        self._outputStream.write(self._delimiter.join(map(str, chunks))+'\n')

class FileReader:
    def __init__(self, inputStream, args):
        self._inputStream = openFile(inputStream, 'r')
        self._delimiter = args.delimiter if args.delimiter else os.environ.get('TOOLBOX_DELIMITER', None)
        header = args.header or os.environ.get('TOOLBOX_HEADER', '').lower() == 'true'
        if header:
            self._header = self._readHeader()
            self.next = self._firstnext
        else:
            self._header = Header()
            self.next = self._next

    @property
    def delimiter(self):
        return self._delimiter

    @property
    def header(self):
        return self._header

    @property
    def hasHeader(self):
        return len(self._header.columns) > 0

    def _readHeader(self):
        preamble = next(self._inputStream)
        return Header(preamble.strip().split(self._delimiter))
        
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def _firstnext(self):
        self.next = self._next
        row = self.next()
        if len(row) != len(self._header):
            sys.stderr.write('Warning: number of rows in input does not match number of rows in header\n')
        return row
        
    def _next(self):
        return next(self._inputStream).strip().split(self._delimiter)

    def readline(self):
        try:
            return self.next()
        except StopIteration:
            return None

    def close(self):
        self._inputStream.close()

    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()

class ParameterParser:
    def __init__(self, descrip, infiles = 1, outfile = True, group = True, columns = 1, append = True, labels = None, ordered = True):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=descrip)
        if infiles == 0:
            pass
        elif infiles == 1:
            self.parser.add_argument('infile', nargs='?', default='-', help='use - for stdin')
        else:
            self.parser.add_argument('infiles', nargs='*', default=['-'], help='use - for stdin')
        if outfile:
            self.parser.add_argument('outfile', nargs='?', default='-', help='use - for stdout')
        if group:
            self.parser.add_argument('-g', '--group', nargs='+', default=[], help='column(s) to group input by')
        if columns == 1:
            self.parser.add_argument('-c', '--column', default=0, help='column to manipulate')
        elif columns != 0:
            self.parser.add_argument('-c', '--columns', nargs='+', default=[0], help='column(s) to manipulate')
        if labels:
            self.parser.add_argument('-l', '--labels', nargs='+', default=labels, help='labels for the column(s)')
        if append:
            self.parser.add_argument('--append', action='store_true', default=False, help='keep original columns in output')
        if ordered:
            self.parser.add_argument('--ordered', action='store_true', default=False, help='input is sorted by group')
        self.parser.add_argument('--delimiter', default=None)
        self.parser.add_argument('--header', action='store_true', default=False)

    def parseArgs(self):
        args = self.parser.parse_args()
        if hasattr(args, 'infile'):
            args.infile = FileReader(args.infile, args)
        elif hasattr(args, 'infiles'):
            args.infiles = [FileReader(infile, args) for infile in args.infiles]
            args.infile = args.infiles[0]
        if hasattr(args, 'group'):
            args.group_names = args.infile.header.names(args.group)
            args.group = args.infile.header.indexes(args.group)
        if hasattr(args, 'columns'):
            args.columns_names = args.infile.header.names(args.columns)
            args.columns = args.infile.header.indexes(args.columns)
        if hasattr(args, 'column'):
            args.column_name = args.infile.header.name(args.column)
            args.column = args.infile.header.index(args.column)
        return args
        
    def getArgs(self, args):
        if hasattr(args, 'outfile'):
            if hasattr(args, 'infile'):
                args.outfile = FileWriter(args.outfile, args.infile, args)
            else:
                args.outfile = FileWriter(args.outfile, None, args)
        return args
