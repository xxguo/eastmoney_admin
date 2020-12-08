# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import xadmin
import datetime
from xlrd import xldate_as_tuple
from .models import SymbolInfo, GubaInfo, GubaDayScore
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


class SymbolInfoResource(resources.ModelResource):

    # import_id_fields = ("name", "description", "pw")

    # def get_export_headers(self):
    #     # 是你想要的导出头部标题headers
    #     return ['员工号', '员工姓名', '公司名称']

    class Meta:
        model = SymbolInfo
        skip_unchanged = True
        raise_errors = True
        # report_skipped = False
        fields = ("symbol_id", "code", "name", "category_type", "status", "a_status", "max_crawl_page",
                  "crawl_level", "sum_count", "crawl_count", "min_publish_time", "min_last_time", "crawl_start_date", "update_time")

        search_fields = ('name', 'symbol_id')
        raw_id_fields = ("id", "symbol_id")
        list_display_links = ("id", "symbol_id")
        readonly_fields = ('id', "symbol_id", "update_time")
        list_editable = ("crawl_level", "max_crawl_page", "status", "a_status")
        paginator = LargeTablePaginator
        import_id_fields = ("symbol_id", )

    def before_import_row(self, row, **kwargs):
        if isinstance(row, dict):
            for key, value in row.items():
                if key == 'crawl_start_date':
                    if isinstance(value, (int, float, long)):
                        value_t = xldate_as_tuple(value, 0)
                        value = datetime.datetime(*value_t).date()
                    elif isinstance(value, datetime.datetime):
                        value = value.date()
                    else:
                        value = parser.parse(value).date()
                    row[key] = unicode(value)

                if isinstance(value, (int, long, float)):
                    row[key] = unicode(value)
        return super(SymbolInfoResource, self).before_import_row(row, **kwargs)

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        return super(SymbolInfoResource, self).save_instance(instance, using_transactions, dry_run)

    def after_save_instance(self, instance, using_transactions, dry_run):
        return super(SymbolInfoResource, self).after_save_instance(instance, using_transactions, dry_run)


@xadmin.sites.register(SymbolInfo)
class SymbolInfoAdmin(object):
    # import_export_args = {'import_resource_class': TesttResource, 'export_resource_class': TesttResource}
    import_export_args = {'import_resource_class': SymbolInfoResource}
    resource_class = SymbolInfoResource
    list_display = ("symbol_id", "code", "name", "category_type", "status", "a_status", "max_crawl_page",
                    "crawl_level", "sum_count", "crawl_count", "min_publish_time", "crawl_start_date", "update_time")
    list_filter = (
        "symbol_id", "category_type", "status", "a_status"
    )
    date_hierarchy = 'crawl_start_date'
    model_icon = "fa fa-check-square"
    list_editable = ("crawl_level", "max_crawl_page", "status", "a_status")
    # reversion_enable = True


@xadmin.sites.register(GubaInfo)
class GubaInfoAdmin(object):
    # readonly_fields = ("post_idss", "symbol_id", "code_name", "title", "content", "from_a", "like_count", "forward_count",
    #               "click_count", "click_count", "publish_time", "last_time", "user_id", "user_age", "user_influ_level",  "content_len")
    list_display = ("post_id", "symbol_id", "code_name", "from_a", "like_count", "forward_count","score", "user_influ_level",
                    "content_len", "publish_time", "last_time")
    readonly_fields = ("post_id", "symbol_id", "code_name", "title", "content", "from_a", "user_id",
                       "user_name", "user_nickname",
                       "user_age", "user_influ_level", "content_len", "publish_time", "last_time")
    list_filter = (
        "publish_time", "symbol_id", "post_id"
    )
    ordering = ("-id", )
    raw_id_fields = ("id", "post_id")


# @xadmin.sites.register(GubaDayScore)
# class GubaDayScoreAdmin(object):
#     list_display = ('dt','symbol_id', 'code', 'category_type', 'total_count', 'good_count', 'bad_count', 'good_score',
#                     'bad_score', 'total_count_7', 'total_count_30')
#
#     list_filter = (
#         "symbol_id", "category_type", "dt"
#     )
#     readonly_fields = ("id", "dt", "symbol_id", "code", "update_time", "create_time")
#     ordering = ("-dt", )
#     model_icon = "fa fa-table"