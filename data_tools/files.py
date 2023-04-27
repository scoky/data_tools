import os
import sys

import re
number_pattern = re.compile("(-?\d+\.?\d*(e[\+|\-]?\d+)?)", re.IGNORECASE)

# Search an input value for a number
def findNumber(value):
    from decimal import Decimal,InvalidOperation
    try:
        return Decimal(value)
    except InvalidOperation:
        try:
            return Decimal(number_pattern.search(value.replace(',', '')).group())
        except AttributeError:
            raise Exception('Value "{0}" does not contain a number'.format(value))

def parseBool(x):
    if x == 'True':
        return True
    elif x == 'False':
        return False
    else: 
        raise ValueError('not a bool')

class ValueInterpreter:
    def __init__(self):
        from decimal import Decimal,InvalidOperation
        import ipaddress
        from collections import OrderedDict
        self._types = OrderedDict()
        self._types['number'] = (Decimal, InvalidOperation)
        self._types['ip'] = (ipaddress.ip_network, ValueError)
        self._types['bool'] = (parseBool, ValueError)
        # type 'string' is not added to the dict because it doesn't need to be parsed
        self._cols = {}

    def interpretCol(self, value, column):
        if column in self._cols:
            # This column has a known type
            interpret_type = self._cols[column]
            # Short circuit strings since no parsing is needed
            if interpret_type == 'string':
                return value
            classFunc, classError = self._types[interpret_type]
            try:
                return classFunc(value)
            except classError:
                # Previous rows had a interpreted type for this column that no longer works for later columns
                raise Exception("Column {} interpretted as {} but '{}' cannot be parsed".format(column, interpret_type, value))
        else:
            # This column has not been encountered before and doesn't have a known type
            value, interpret_type = self.interpret(value)
            # Save the type for future parsing
            self._cols[column] = interpret_type
            return value

    def interpret(self, value):
        for name,data in self._types.items():
            classFunc, classError = data
            try:
                return classFunc(value), name
            except classError:
                pass
        # Return uninterpretted (as string)
        return value, 'string'

def concatFiles(files, opts='r'):
    for f in files:
        for line in openFile(f, opts):
            yield line

def fileRange(startFile, endFile):
    startDir, startFile = os.path.split(startFile)
    _, endFile = os.path.split(endFile)
    import glob
    if startDir == '':
        files = glob.iglob('*');
    else:
        files = glob.iglob(os.path.expanduser(startDir) + '/*');
    ret = []
    for fn in files:
        if startFile <= os.path.basename(fn) <= endFile:
            ret.append(fn)
    return sorted(ret)

def openFile(filename, opts, **kwargs):
    import io
    if type(filename) is str:
        if filename == '-':
            return sys.stdin if opts == 'r' else sys.stdout
        else:
            import gzip
            return gzip.open(os.path.expanduser(filename), opts+'t', **kwargs) if filename.endswith('.gz') else open(os.path.expanduser(filename), opts, **kwargs)
    elif isinstance(filename, io.IOBase):
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
                if len(self.columns) == 0:
                    return None
                raise ValueError("Invalid column '%s' specified" % colName) from e

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
        from copy import copy
        return Header(copy(self.columns))

class FileWriter:
    def __init__(self, outputStream, reader, args, opts = 'w'):
        self._fileStream = openFile(outputStream, opts, newline='')
        self._delimiter = args.delimiter if args.delimiter else os.environ.get('TOOLBOX_DELIMITER', ' ')
        self._quotechar = args.quotechar if args.quotechar else os.environ.get('TOOLBOX_QUOTECHAR', '"')
        import csv
        self._outputStream = csv.writer(self._fileStream, delimiter=self._delimiter, quotechar=self._quotechar, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
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
        try:
            self._outputStream.writerow(chunks)
        except BrokenPipeError:
            sys.exit(1)

class FileReader:
    def __init__(self, inputStream, args):
        self._delimiter = args.delimiter if args.delimiter else os.environ.get('TOOLBOX_DELIMITER', ' ')
        if self._delimiter == r'\t': # Handle special characters
            self._delimiter = '\t'
        self._quotechar = args.quotechar if args.quotechar else os.environ.get('TOOLBOX_QUOTECHAR', '"')
        self._fileStream = openFile(inputStream, 'r', newline='')
        import csv
        self._inputStream = csv.reader(self._fileStream, delimiter=self._delimiter, quotechar=self._quotechar, skipinitialspace=True)
        header = args.header if not args.header is None else (os.environ.get('TOOLBOX_HEADER', '').lower() == 'true')
        if header:
            self._header = self._readHeader()
            self._next = self._firstnext
        else:
            self._header = Header()
            self._next = self._secondnext

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
        try:
            preamble = next(self._inputStream)
        except StopIteration:
            # No rows
            preamble = []
        return Header(preamble)
        
    def __iter__(self):
        return self

    def __next__(self):
        return self._next()

    def _firstnext(self):
        self._next = self._secondnext
        row = next(self)
        if len(row) != len(self._header):
            sys.stderr.write('Warning: number of rows in input does not match number of rows in header\n')
        return row

    def _secondnext(self):
        return next(self._inputStream) # TODO: Interpolate types? str, int, float, decimal, ipaddress

    def readline(self):
        try:
            return next(self)
        except StopIteration:
            return None

    def close(self):
        pass
        self._fileStream.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

class ParameterParser:
    def __init__(self, descrip, infiles = 1, outfile = True, group = True, columns = 1, append = True, labels = None, ordered = True):
        import argparse
        self.parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=descrip)
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
        self.parser.add_argument('--delimiter', default=None, help='if not specified, env TOOLBOX_DELIMITER or whitespace is used')
        self.parser.add_argument('--quotechar', default=None, help='if not specified, env TOOLBOX_QUOTECHAR or " is used')
        self.parser.add_argument('--header', action='store_true', default=None, help='override env TOOLBOX_HEADER')
        self.parser.add_argument('--no-header', action='store_false', dest='header', help='override env TOOLBOX_HEADER')

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
