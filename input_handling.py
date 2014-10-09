#!/usr/bin/python

import logging
import argparse
import sys
import traceback
import os
import re
from decimal import Decimal
from decimal import InvalidOperation

number_pattern = re.compile("(-?\d+\.?\d*)")

# Search an input value for a number
def findNumber(value):
   try:
     return Decimal(value)
   except InvalidOperation as e:
     return Decimal(number_pattern.search(value).group())

