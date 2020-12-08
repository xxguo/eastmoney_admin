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


# @python_2_unicode_compatible
class SymbolInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol_id = models.IntegerField(verbose_name='股票号')
    code = models.CharField(max_length=10, verbose_name='股票代码')
    name = models.CharField(max_length=20, verbose_name='股票名称')
    category_type = models.IntegerField(verbose_name='分类')
    status = models.SmallIntegerField(choices=CRAWL_STATUS, verbose_name='抓取状态')
    a_status = models.SmallIntegerField(choices=A_STATUS, verbose_name='分析状态')
    max_crawl_page = models.IntegerField(verbose_name='抓取最大页数')
    crawl_level = models.IntegerField(verbose_name='抓取优先级')
    sum_count = models.IntegerField(verbose_name='总数')
    crawl_count = models.IntegerField(verbose_name='实际抓取数')
    min_publish_time = models.DateField(verbose_name='已抓发布日期')
    min_last_time = models.DateField(verbose_name='已抓更新日期')
    crawl_start_date = models.DateField(verbose_name='抓取最早日期')
    update_time = models.DateTimeField(verbose_name='最近更新日期')

    def __repr__(self):
        return self.symbol_id

    def __str__(self):
        return self.symbol_id

    def __unicode__(self):
        return u"{0}".format(self.symbol_id)

    class Meta:
        app_label = 'cms'
        db_table = 'symbol_info'
        verbose_name = u"股票抓取信息"
        verbose_name_plural = verbose_name


# @python_2_unicode_compatible
class GubaInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    post_id = models.IntegerField(verbose_name='文章ID')
    symbol_id = models.IntegerField(verbose_name='股票号')
    code_name = models.CharField(max_length=20, verbose_name='股票名称')
    title = models.CharField(max_length=50, verbose_name='文章标题', blank=True)
    content = models.TextField(verbose_name='正文')
    from_a = models.CharField(max_length=16, verbose_name='来源', db_column='from')
    like_count = models.IntegerField(verbose_name='喜欢数')
    forward_count = models.IntegerField(verbose_name='转发数')
    click_count = models.IntegerField(verbose_name='阅读数')
    comment_count = models.IntegerField(verbose_name='评论数')
    publish_time = models.DateTimeField(verbose_name='发布日期')
    last_time = models.DateTimeField(verbose_name='更新日期')
    user_id = models.IntegerField(verbose_name='用户ID')
    user_name = models.CharField(max_length=16, verbose_name='用户名')
    user_nickname = models.CharField(max_length=16, verbose_name='用户昵称')
    user_age = models.CharField(max_length=16, verbose_name='用户昵称')
    user_influ_level = models.IntegerField(verbose_name='用户影响力')
    score = models.FloatField(verbose_name='情感评分')
    content_len = models.IntegerField(verbose_name='文本长度')

    def __repr__(self):
        return unicode(self.code_name)

    def __str__(self):
        return str(self.code_name)

    class Meta:
        app_label = 'cms'
        db_table = 'guba_info'
        verbose_name = u"股吧数据信息"
        verbose_name_plural = verbose_name

# @python_2_unicode_compatible
class GubaDayScore(models.Model):
    id = models.BigAutoField(primary_key=True)
    dt = models.DateField(verbose_name='日期')
    symbol_id = models.IntegerField(verbose_name='股票号')
    code = models.CharField(max_length=16, verbose_name='股票名称')
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
        app_label = 'cms'
        db_table = 'guba_day_score'
        verbose_name = u"股吧个股统计"
        verbose_name_plural = verbose_name