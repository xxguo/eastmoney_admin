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

TRADE_DATE_STATUS = (
    (1, 'Y'),
    (0, 'N'),
)

CATEGORY_TYPE = (
    (1, '医药板块'),
    (300, '沪深300'),
    (500, '中证500'),
    (1000, '中证1000'),
    (0, 'A股'),
)

# @python_2_unicode_compatible
class GubaDayScore(models.Model):
    id = models.BigAutoField(primary_key=True)
    dt = models.DateField(verbose_name='日期')
    symbol_id = models.IntegerField(verbose_name='股票号')
    code = models.CharField(max_length=16, verbose_name='股票名称')
    is_trad_date = models.IntegerField(choices=TRADE_DATE_STATUS, verbose_name='交易日')
    category_type = models.IntegerField(verbose_name='分类')
    total_count = models.IntegerField(verbose_name='总数')
    good_count = models.IntegerField(verbose_name='good数')
    bad_count = models.IntegerField(verbose_name='bad数')
    good_score = models.FloatField(verbose_name='good分')
    bad_score = models.FloatField(verbose_name='good分')

    total_count_7 = models.IntegerField(verbose_name='7日总数')
    good_count_7 = models.IntegerField(verbose_name='7日good数')
    bad_count_7 = models.IntegerField(verbose_name='7日bad数')
    good_score_7 = models.FloatField(verbose_name='7日good分')
    bad_score_7 = models.FloatField(verbose_name='7日good分')

    total_count_30 = models.IntegerField(verbose_name='30日总数')
    good_count_30 = models.IntegerField(verbose_name='30日good数')
    bad_count_30 = models.IntegerField(verbose_name='30日bad数')
    good_score_30 = models.FloatField(verbose_name='30日good分')
    bad_score_30 = models.FloatField(verbose_name='30日good分')

    update_time = models.DateTimeField(verbose_name='更新日期')
    create_time = models.DateTimeField(verbose_name='创建日期')


    def __repr__(self):
        return self.symbol_id

    def __str__(self):
        return self.symbol_id

    def __unicode__(self):
        return unicode(self.symbol_id)

    class Meta:
        app_label = 'statistics'
        db_table = 'guba_day_score'
        verbose_name = u"股吧个股统计"
        verbose_name_plural = verbose_name


class GubaDayABScore(models.Model):
    id = models.BigAutoField(primary_key=True)
    dt = models.DateField(verbose_name='日期')
    symbol_id = models.IntegerField(verbose_name='股票号')
    code = models.CharField(max_length=16, verbose_name='股票名称')
    is_trad_date = models.IntegerField(choices=TRADE_DATE_STATUS, verbose_name='交易日')
    category_type = models.IntegerField(verbose_name='分类')
    total_count = models.IntegerField(verbose_name='总数')
    good_count = models.IntegerField(verbose_name='good数')
    bad_count = models.IntegerField(verbose_name='bad数')
    good_a_score = models.FloatField(verbose_name='good_a_分')
    good_b_score = models.FloatField(verbose_name='good_b_分')
    bad_a_score = models.FloatField(verbose_name='bad_a_分')
    bad_b_score = models.FloatField(verbose_name='bad_b_分')

    total_count_7 = models.IntegerField(verbose_name='7日总数')
    good_count_7 = models.IntegerField(verbose_name='7日good数')
    bad_count_7 = models.IntegerField(verbose_name='7日bad数')
    good_a_score_7 = models.FloatField(verbose_name='7日a_good分')
    good_b_score_7 = models.FloatField(verbose_name='7日b_good分')
    bad_a_score_7 = models.FloatField(verbose_name='7日a_bad分')
    bad_b_score_7 = models.FloatField(verbose_name='7日b_bad分')

    total_count_30 = models.IntegerField(verbose_name='30日总数')
    good_count_30 = models.IntegerField(verbose_name='30日good数')
    bad_count_30 = models.IntegerField(verbose_name='30日bad数')
    good_a_score_30 = models.FloatField(verbose_name='30日a_good分')
    good_b_score_30 = models.FloatField(verbose_name='30日b_good分')
    bad_a_score_30 = models.FloatField(verbose_name='30日a_bad分')
    bad_b_score_30 = models.FloatField(verbose_name='30日b_bad分')

    update_time = models.DateTimeField(verbose_name='更新日期')
    create_time = models.DateTimeField(verbose_name='创建日期')

    def __repr__(self):
        return self.symbol_id

    def __str__(self):
        return self.symbol_id

    def __unicode__(self):
        return unicode(self.symbol_id)

    class Meta:
        app_label = 'statistics'
        db_table = 'guba_day_a_b_score'
        verbose_name = u"(两指标)股吧个股统计"
        verbose_name_plural = verbose_name


class GubaTradingCategoryScore(models.Model):
    id = models.BigAutoField(primary_key=True)
    dt = models.DateField(verbose_name='日期')
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='分类')
    total_count = models.IntegerField(verbose_name='总数')
    good_count = models.IntegerField(verbose_name='good数')
    bad_count = models.IntegerField(verbose_name='bad数')
    good_score = models.FloatField(verbose_name='good分')
    bad_score = models.FloatField(verbose_name='bad分')

    total_count_5 = models.IntegerField(verbose_name='5日总数')
    good_count_5 = models.IntegerField(verbose_name='5日good数')
    bad_count_5 = models.IntegerField(verbose_name='5日bad数')
    good_score_5 = models.FloatField(verbose_name='5日good分')
    bad_score_5 = models.FloatField(verbose_name='5日bod分')

    total_count_20 = models.IntegerField(verbose_name='20日总数')
    good_count_20 = models.IntegerField(verbose_name='20日good数')
    bad_count_20 = models.IntegerField(verbose_name='20日bad数')
    good_score_20 = models.FloatField(verbose_name='20日good分')
    bad_score_20 = models.FloatField(verbose_name='20日bod分')

    update_time = models.DateTimeField(verbose_name='更新日期')
    create_time = models.DateTimeField(verbose_name='创建日期')


    def __repr__(self):
        return self.symbol_id

    def __str__(self):
        return self.symbol_id

    def __unicode__(self):
        return unicode(self.symbol_id)

    class Meta:
        app_label = 'statistics'
        db_table = 'guba_trading_category_score'
        verbose_name = u"交易日汇总统计"
        verbose_name_plural = verbose_name


class GubaABTradingCategoryScore(models.Model):
    id = models.BigAutoField(primary_key=True)
    dt = models.DateField(verbose_name='日期')
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name='分类')
    total_count = models.IntegerField(verbose_name='总数')
    good_count = models.IntegerField(verbose_name='good数')
    bad_count = models.IntegerField(verbose_name='bad数')
    good_a_score = models.FloatField(verbose_name='good_a分')
    good_b_score = models.FloatField(verbose_name='good_b分')
    bad_a_score = models.FloatField(verbose_name='bad_a分')
    bad_b_score = models.FloatField(verbose_name='bad_b分')

    total_count_5 = models.IntegerField(verbose_name='5日总数')
    good_count_5 = models.IntegerField(verbose_name='5日good数')
    bad_count_5 = models.IntegerField(verbose_name='5日bad数')
    good_a_score_5 = models.FloatField(verbose_name='5日good_a分')
    good_b_score_5 = models.FloatField(verbose_name='5日good_b分')
    bad_a_score_5 = models.FloatField(verbose_name='5日bod_a分')
    bad_b_score_5 = models.FloatField(verbose_name='5日bod_b分')

    total_count_20 = models.IntegerField(verbose_name='20日总数')
    good_count_20 = models.IntegerField(verbose_name='20日good数')
    bad_count_20 = models.IntegerField(verbose_name='20日bad数')
    good_a_score_20 = models.FloatField(verbose_name='20日good_a分')
    good_b_score_20 = models.FloatField(verbose_name='20日good_b分')
    bad_a_score_20 = models.FloatField(verbose_name='20日bod_a分')
    bad_b_score_20 = models.FloatField(verbose_name='20日bod_b分')

    update_time = models.DateTimeField(verbose_name='更新日期')
    create_time = models.DateTimeField(verbose_name='创建日期')


    def __repr__(self):
        return self.symbol_id

    def __str__(self):
        return self.symbol_id

    def __unicode__(self):
        return unicode(self.symbol_id)

    class Meta:
        app_label = 'statistics'
        db_table = 'guba_ab_trading_category_score'
        verbose_name = u"(两指标)交易日汇总统计"
        verbose_name_plural = verbose_name