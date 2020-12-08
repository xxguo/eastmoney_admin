# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from xlrd import xldate_as_tuple
from django.test import TestCase
import datetime

# Create your tests here.
from xlrd import xldate_as_tuple

from dateutil import parser
a = xldate_as_tuple(43466.0, 0)
print a
value = datetime.datetime(*a)
c = parser.parse(str(value)).date()

b = 43466.0
print type(b)

print type(c)
print unicode(c)
import openpyxl

openpyxl.load_workbook()
