# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import xadmin
import datetime
from xlrd import xldate_as_tuple
from dateutil import parser
from import_export import resources
from .models import SymbolCons500, SymbolCons300, SymbolConsYiYAO, SymbolCons1000
# Register your models here.


class SymbolCons500Resource(resources.ModelResource):
    class Meta:
        skip_unchanged = True
        model = SymbolCons500
        fields = ("dt", "symbol_id", "code", "code_name", "category_type")
        import_id_fields = ("dt", "business", "coop_company", "product_name", "unit_price_time")

    def before_import_row(self, row, **kwargs):
        if isinstance(row, dict):
            # print '===============', row
            for key, value in row.items():
                if key == 'dt':
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
        return super(SymbolCons500Resource, self).before_import_row(row, **kwargs)


@xadmin.sites.register(SymbolCons500)
class SymbolCons500Admin(object):

    import_export_args = {'import_resource_class': SymbolCons500Resource}
    resource_class = SymbolCons500Resource
    list_display = ("dt", "symbol_id", "code", "code_name", "category_type", "weight", "create_time", "update_time")

    # fieldsets = (
    #     ("确定唯一组合", {'fields': ('dt', "business", "coop_company", "product_name")}),
    #     ("参数", {'fields': ('period', 'unit_price_time', 'charging_mode', 'monthly_cost')})
    # )

    list_display_links = ("dt", "symbol_id")

    readonly_fields = ('id', "symbol_id", "code", "code_name", "create_time", "update_time")

    search_fields = ["code", "code_name"]
    list_filter = [
        "dt", "symbol_id", "update_time"
    ]
    reversion_enable = True
    ordering = ("-dt", )
    model_icon = "fa fa-list"


@xadmin.sites.register(SymbolCons300)
class SymbolCons300Admin(object):
    list_display_links = ("dt", "symbol_id")
    list_display = ("dt", "symbol_id", "code", "code_name", "category_type", "weight", "create_time", "update_time")
    readonly_fields = ('id', "symbol_id", "code", "code_name", "create_time", "update_time")

    search_fields = ["code", "code_name"]
    list_filter = [
       "dt", "symbol_id", "update_time"
    ]
    reversion_enable = True
    ordering = ("-dt", )
    model_icon = "fa fa-list"


@xadmin.sites.register(SymbolConsYiYAO)
class SymbolConsYiYAOAdmin(object):
    list_display_links = ("dt", "symbol_id")
    list_display = ("dt", "symbol_id", "code", "code_name", "category_type", "create_time", "update_time")
    readonly_fields = ('id', "symbol_id", "code", "code_name", "create_time", "update_time")

    search_fields = ["code", "code_name"]
    list_filter = [
       "dt", "symbol_id", "update_time"
    ]
    reversion_enable = True
    ordering = ("-dt", )
    model_icon = "fa fa-list"


@xadmin.sites.register(SymbolCons1000)
class SymbolCons1000Admin(object):
    list_display_links = ("dt", "symbol_id")
    list_display = ("dt", "symbol_id", "code", "code_name", "category_type", "weight", "create_time", "update_time")
    readonly_fields = ('id', "symbol_id", "code", "code_name", "create_time", "update_time")

    search_fields = ["code", "code_name"]
    list_filter = [
       "dt", "symbol_id", "update_time"
    ]
    reversion_enable = True
    ordering = ("-dt", )
    model_icon = "fa fa-list"
Wo1176868066