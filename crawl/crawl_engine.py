# -*- coding: utf-8 -*-
# @Time    : 3/31/20 7:16 AM
# @Author  : xxguo
# @Software: PyCharm
import time
import random
import requests
import datetime
from snownlp import SnowNLP
from bs4 import BeautifulSoup
from .crawlbase import CrawlerBase
from db.mysql.connection import MysqlConnection
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib3
urllib3.disable_warnings()
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


web_headers = {
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Host': 'guba.eastmoney.com',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://guba.eastmoney.com/remenba.aspx?type=1&tab=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
}

api_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Host": "mguba.eastmoney.com",
    "Origin": "https://mguba.eastmoney.com",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}


class CrawlEastmoney(CrawlerBase):
    def __init__(self):
        self.stock_collection_dict = dict()
        self.conn = MysqlConnection()

    def insert_symbol_data(self, symbol, name):
        sql = "select * from symbol_info where code='{0}'"


    def update_symbol_data_max_num(self, sum_count, symbol_id):
        update_sql = "update symbol_info set sum_count = {0} where symbol_id={1};".format(sum_count, symbol_id)
        result = self.conn.update(update_sql)
        print "symbol: {0} sum coumt-------------{1},  {2}".format(symbol_id, sum_count, result)

    def insert_guba(self, data=None, data_list=None, name=None):
        if data:
            post_id = data['post_id']
            print 'insert data----', post_id, datetime.datetime.now()
            query_sql = "select id from guba_info where  post_id='{0}'".format(post_id)
            is_exist = self.conn.getOne(query_sql)
            if is_exist:
                print '======== cun zai le ', post_id
            else:
                key_field = data.keys()
                key_len = len(key_field)
                values_list = data.values()
                insert_sql = "insert into guba_info ({0}) values ({1})".format(
                    ','.join(key_field), ','.join(['%s'] * key_len))
                _id = self.conn.insertOne(insert_sql, tuple(values_list))
                map(lambda x: str(x), values_list)

                print 'new ----- _id', _id
        elif data_list:
            values_list = []
            first_data = data_list[0]
            key_field = first_data.keys()
            key_len = len(key_field)
            insert_sql = "insert IGNORE into guba_info ({0}) values ({1})".format(
                    ','.join(key_field), ','.join(['%s'] * key_len))
            for data in data_list:
                values_list.append(data.values())
            insert_count = self.conn.insertMany(insert_sql, values_list)
            print "insert =============== {0} count: {1}, {2}".format(name, insert_count, len(data_list))
            del data_list

    def get_task_symbol(self):
        try_count = 0
        while 1:
            try_count += 1
            q_sql = "select  id, code, max_crawl_page, crawl_start_date from symbol_info where `status` = 0 order by crawl_level desc limit 4"
            result = self.conn.getAll(q_sql)
            if not result:
                sleep_len = try_count * 3 if try_count < 100 else 60 * 60
                print '--------task null,  try_count:{0}, now:{1}, sleep_time:{2}'.format(try_count, datetime.datetime.now(), sleep_len)
                time.sleep(sleep_len)
                continue
            break

        code, max_crawl_page, crawl_start_date = random.choice(map(lambda x: (x['code'], x['max_crawl_page'], x['crawl_start_date']), result))
        self.conn.update("update  symbol_info  set `status` = 1 where code='{0}'".format(code))
        c_sql = "SELECT count(1) c FROM guba_info where symbol_id= {0}".format(code)
        result = self.conn.getOne(c_sql)
        if result:
            c = result.get("c")
            print "++++++++++++++c----------", c
        else:
            c = 0
        return code, c, max_crawl_page, str(crawl_start_date)

    def run(self):
        # obj_iter = self._init_web_home()
        # for symbol, symbo_name in obj_iter:
        #     pass
        # self.crawl_stock_article('600007')
        while 1:
            code, already_count, max_crawl_page, crawl_start_date = self.get_task_symbol()
            try:
                self.crawl_stock_article(code, page=1, page_size=100, max_page=120, already_count=already_count,
                                         max_crawl_page=max_crawl_page, crawl_start_date=crawl_start_date)
                self.conn.update("update  symbol_info  set `status` = 2 where code='{0}'".format(code))
            except Exception as e:
                self.conn.update("update  symbol_info  set `status` = 3 where code='{0}'".format(code))
                import traceback
                print traceback.format_exc()
                continue

    def crawl_stock_article(self, symbol, page=1, page_size=100, max_page=1, already_count=0, max_crawl_page=300,
                            crawl_start_date='2016-01-01'):
        time.sleep(random.randint(0, 3))
        if page > max_crawl_page or page > max_page:
            print 'success==============', symbol, ' ', page
            return None
        else:
            print 'running------', symbol, ' ', page
        url = "https://mguba.eastmoney.com/interface/GetData.aspx?mt={0}".format(time.time())
        post_data = {
            "path": "/webarticlelist/api/Article/ArticleListForMobile",
            "env:": 2,
            "param": "code={0}&type=0&p={1}&ps={2}&sorttype=1".format(symbol, page, page_size)
        }
        api_headers['Referer'] = 'https://mguba.eastmoney.com/mguba/list/600018?from=BaiduAladdin'
        try_count = 0
        is_stop_crawl = False
        while 1:
            try:
                req = requests.post(url, data=post_data, headers=api_headers, timeout=5, verify=False)
                break
            except Exception as e:
                try_count += 1
                time.sleep(2*try_count)
                print "error+++++++", symbol, try_count, e
                if try_count > 3:
                    is_stop_crawl = True
                    break
        if is_stop_crawl:
            return

        data_dict = req.json()
        if page <= 1:
            count = data_dict.get("count")

            self.update_symbol_data_max_num(count, symbol)

            max_page = count / page_size + 1 if count % page_size > 0 else 0
            max_page = min(max_page, max_crawl_page)

            if already_count > 1000:
                already_count *= 1.2
            already_page = already_count / page_size
            already_page = int(already_page)
            if already_page > 1:
                page = int(already_page)
                print "already_page crawl +++++++++++++++", page

        data_list = []
        for item in data_dict['re']:
            if item['post_type'] != 0:
                continue
            user_info = item.get("post_user", {})
            post_content = item.get("post_content") or item.get("post_title")
            if not post_content:
                continue
            try:
                score = SnowNLP(post_content).sentiments
            except Exception as e:
                score = 0.5

            if item['post_last_time'] <= '2000-01-01':
                continue
            elif item['post_last_time'] and item['post_last_time'] <= crawl_start_date:
                max_crawl_page = max_page = page

            try:
                user_id = int(user_info.get("user_id"))
            except:
                user_id = 0
            data = {
                "post_id": item['post_id'],
                "symbol_id": symbol,
                "title": "",
                "content": item['post_content'],
                'code_name': item['code_name'],
                "`from`": item['post_from'],
                "like_count": item['post_like_count'],
                "forward_count": item['post_forward_count'],
                "click_count": item['post_click_count'],
                "comment_count": item['post_comment_count'],
                "publish_time": item['post_publish_time'],
                "last_time": item['post_last_time'],
                "user_id": user_id,
                "user_name": user_info.get("user_name"),
                "user_nickname": user_info.get("user_nickname"),
                "user_age": user_info.get("user_age"),
                "user_influ_level": user_info.get("user_influ_level"),
                "score": score,
                "content_len": len(post_content)
            }
            data_list.append(data)
        self.insert_guba(data_list=data_list, name=symbol)

        self.crawl_stock_article(symbol, page=page+1, page_size=page_size, max_page=max_page,
                                 max_crawl_page=max_crawl_page)

    def _init_web_home(self):
        url_list = ['http://guba.eastmoney.com/remenba.aspx?type=1&tab=2']
        for url in url_list:
            req = requests.get(url, headers=web_headers, timeout=5)
            soup = BeautifulSoup(req.content)
            a_list = soup.find('div', 'ngbglistdiv').find_all('a')
            print '=start--------', len(a_list)
            for item in a_list:
                href = item.get('href', None)
                if not href:
                    continue

                symbol = href[5:-5]
                yield symbol, item.get_text()

    def init_data_symbol(self):
        url_list = ['http://guba.eastmoney.com/remenba.aspx?type=1&tab=2']
        for url in url_list:
            req = requests.get(url, headers=web_headers, timeout=10)
            soup = BeautifulSoup(req.content)
            a_list = soup.find('div', 'ngbglistdiv').find_all('a')
            print '=start--------', len(a_list)
            for item in a_list:
                href = item.get('href', None)
                if not href:
                    continue

                symbol = href[5:-5]
                q_sql = "select  *  from symbol_info where symbol_id='{0}'".format(symbol)
                a = self.conn.getOne(q_sql)
                if a:
                    continue
                sql = "insert into symbol_info (symbol_id, code, `name`) VALUES ('{0}', '{0}', '{1}')".format(symbol, item.get_text())
                self.conn.insertOne(sql)
                # yield symbol, item.get_text()

