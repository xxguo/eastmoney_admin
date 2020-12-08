# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

CRAWL_STATUS = (
    (0, '未启动'),
    (1, '抓取中'),
    (2, '抓取完成'),
    (3, '抓取异常'),
)

A_STATUS = (
    (0, '未分析'),
    (1, '分析中'),
    (2, '分析完成'),
    (3, '分析异常'),
)

CATEGORY_TYPE = (
    (1, '医药板块'),
    (300, '沪深300'),
    (500, '中证500'),
    (1000, '中证1000'),
    (0, 'A股'),
)


# @python_2_unicode_compatible
class SymbolCons500(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol_id = models.IntegerField(verbose_name='股票号')
    code = models.CharField(max_length=10, verbose_name='股票代码')
    code_name = models.CharField(max_length=10, verbose_name='股票名称')
    category_type = models.IntegerField(verbose_name='分类')
    weight = models.FloatField(verbose_name='权重')
    dt = models.DateField(verbose_name='日期')
    create_time = models.DateTimeField(verbose_name='创建日期')
    update_time = models.DateTimeField(verbose_name='更新日期')

    def __repr__(self):
        return self.symbol_id

    def __str__(self):
        return self.symbol_id

    def __unicode__(self):
        return u"{0}".format(self.symbol_id)

    class Meta:
        app_label = 'symbol_cons'
        db_table = 'symbol_cons_500'
        verbose_name = u"中证500成份"
        verbose_name_plural = verbose_name


class SymbolCons300(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol_id = models.IntegerField(verbose_name='股票号')
    code = models.CharField(max_length=10, verbose_name='股票代码')
    code_name = models.CharField(max_length=10, verbose_name='股票名称')
    category_type = models.IntegerField(verbose_name='分类')
    weight = models.FloatField(verbose_name='权重')
    dt = models.DateField(verbose_name='日期')
    create_time = models.DateTimeField(verbose_name='创建日期')
    update_time = models.DateTimeField(verbose_name='更新日期')

    def __repr__(self):
        return self.symbol_id

    def __str__(self):
        return self.symbol_id

    def __unicode__(self):
        return u"{0}".format(self.symbol_id)

    class Meta:
        app_label = 'symbol_cons'
        db_table = 'symbol_cons_300'
        verbose_name = u"沪深300成份"
        verbose_name_plural = verbose_name


class SymbolConsYiYAO(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol_id = models.IntegerField(verbose_name='股票号')
    code = models.CharField(max_length=10, verbose_name='股票代码')
    code_name = models.CharField(max_length=10, verbose_name='股票名称')
    category_type = models.IntegerField(verbose_name='分类')
    dt = models.DateField(verbose_name='日期')
    create_time = models.DateTimeField(verbose_name='创建日期')
    update_time = models.DateTimeField(verbose_name='更新日期')

    def __repr__(self):
        return self.symbol_id

    def __str__(self):
        return self.symbol_id

    def __unicode__(self):
        return u"{0}".format(self.symbol_id)

    class Meta:
        app_label = 'symbol_cons'
        db_table = 'symbol_cons_yiyao'
        verbose_name = u"医药板块成份"
        verbose_name_plural = verbose_name


class SymbolCons1000(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol_id = models.IntegerField(verbose_name='股票号')
    code = models.CharField(max_length=10, verbose_name='股票代码')
    code_name = models.CharField(max_length=10, verbose_name='股票名称')
    category_type = models.IntegerField(verbose_name='分类')
    weight = models.FloatField(verbose_name='权重')
    dt = models.DateField(verbose_name='日期')
    create_time = models.DateTimeField(verbose_name='创建日期')
    update_time = models.DateTimeField(verbose_name='更新日期')

    def __repr__(self):
        return self.symbol_id

    def __str__(self):
        return self.symbol_id

    def __unicode__(self):
        return u"{0}".format(self.symbol_id)

    class Meta:
        app_label = 'symbol_cons'
        db_table = 'symbol_cons_1000'
        verbose_name = u"中证1000成份"
        verbose_name_plural = verbose_name