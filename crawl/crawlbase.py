# coding:utf-8
import requests
import datetime
import json
import requests
import logging
# from app_crawl.settings import APP_POST_URL
# from spider_crawler.core.proxy import proxies


logger = logging.getLogger('app')


class Base(object):
    def __init__(self):
        self.current_time = datetime.datetime.now()

    def crawl(self):
        raise NotImplemented

    @staticmethod
    def _get_requests():
        return requests.session()


class CrawlerBase(Base):
    def __init__(self, proxies=None):
        super(CrawlerBase, self).__init__()
        self.s = self._get_requests()

        self.proxies = proxies

    @staticmethod
    def get_proxy():
        try:
            ip_proxies = proxies(types='weight')
            if ip_proxies:
                req = requests.get("https://www.baidu.com/cache/global/img/gs.gif", proxies=ip_proxies, timeout=1)
                if req.headers.get('Content-Length') == '91':
                        return ip_proxies
        except Exception, e:
            print '代理发生异常', e

        return

    @staticmethod
    def push_app_data(data):
        headers = {
            'Connection': 'close'
        }
        req = requests.post(APP_POST_URL, data=data, headers=headers, timeout=5)
        obj_json = json.loads(req.content)
        if obj_json['code'] == 0:
            return True
        else:
            return False