# -*- coding: utf-8 -*-
# @Time    : 4/13/20 6:11 AM
# @Author  : xxguo
# @Software: PyCharm
import pandas as pd
from db.mysql.connection import MysqlConnection

conn = MysqlConnection()


def get_task():
    result = conn.getAll("select symbol_id from symbol_info where status=2")
    return map(lambda x: x['symbol_id'], result)

for symbol_id in get_task():
    result = conn.getOne("select count(1) t, min(publish_time) publish_time, min(last_time) last_time from guba_info where symbol_id={0} and last_time > '20001-01-01';".format(symbol_id))
    print '--------', symbol_id, result
    sql = "update symbol_info set crawl_count = {0}, min_publish_time= '{1}', min_last_time = '{2}' where symbol_id={3};".format(
        result['t'], result['publish_time'], result['last_time'], symbol_id
    )
    a = update_count = conn.update(sql)
    print '执行结果---------', a



