# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import xadmin
import datetime
from xlrd import xldate_as_tuple
from .models import  GubaDayScore, GubaTradingCategoryScore, GubaDayABScore, GubaABTradingCategoryScore
from dateutil import parser
from django.core.paginator import Paginator, cached_property
from import_export import resources


class LargeTablePaginator(Paginator):
    def _get_count(self):
        return 67

    @cached_property
    def count(self):
        return 33
    # count = property(_get_count)


@xadmin.sites.register(GubaDayABScore)
class GubaDayScoreAdmin(object):
    list_display = ('dt','symbol_id', 'code', 'is_trad_date', 'total_count', 'good_count', 'bad_count', 'good_a_score',
                    'good_b_score', 'bad_a_score', 'bad_b_score', 'total_count_7', 'total_count_30')

    list_filter = (
        "symbol_id", "category_type", "dt"
    )
    readonly_fields = ("id", "dt", "symbol_id", "code", "update_time", "create_time")
    ordering = ("-dt", )
    model_icon = "fa fa-table"


@xadmin.sites.register(GubaDayScore)
class GubaDayScoreAdmin(object):
    list_display = ('dt','symbol_id', 'code', 'is_trad_date', 'total_count', 'good_count', 'bad_count', 'good_score',
                    'bad_score', 'total_count_7', 'total_count_30')

    list_filter = (
        "symbol_id", "category_type", "dt"
    )
    readonly_fields = ("id", "dt", "symbol_id", "code", "update_time", "create_time")
    ordering = ("-dt", )
    model_icon = "fa fa-table"

@xadmin.sites.register(GubaTradingCategoryScore)
class GubaTradingCategoryScoreAdmin(object):
    list_display = ('dt',"category_type", 'total_count', 'good_count', 'bad_count', 'good_score',
                    'bad_score', 'total_count_5', 'total_count_20')

    list_filter = (
        "category_type", "dt"
    )
    readonly_fields = ("id", "dt", "symbol_id", "code", "update_time", "create_time")
    ordering = ("-dt", )
    model_icon = "fa fa-table"


@xadmin.sites.register(GubaABTradingCategoryScore)
class GGubaABTradingCategoryScoreAdmin(object):
    list_display = ('dt',"category_type", 'total_count', 'good_count', 'bad_count', 'good_a_score', 'good_b_score',
                    'bad_a_score', 'bad_b_score', 'total_count_5', 'total_count_20')

    list_filter = (
        "category_type", "dt"
    )
    readonly_fields = ("id", "dt", "symbol_id", "code", "update_time", "create_time")
    ordering = ("-dt", )
    model_icon = "fa fa-table"