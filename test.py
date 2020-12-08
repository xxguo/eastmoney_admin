# -*- coding: utf-8 -*-
# @Time    : 4/4/20 6:35 AM
# @Author  : xxguo
# @Software: PyCharm

import sys

import pandas as pd
from db.mysql.connection import MysqlConnection

conn = MysqlConnection()
reload(sys)
sys.setdefaultencoding('utf8')

a = pd.date_range("20170101", "20200515",  freq='M')
b = pd.date_range("20170101", "20200415", freq='MS')

c = zip(b.to_list(), a.to_list())
b = 1
for start, end in c:
    sql = """
    update symbol_cons_1000 a LEFT JOIN (select symbol_id, weight from cons_1000 where dt='{0}') as b
on a.symbol_id = b.symbol_id
set a.weight = b.weight
where a.dt between '{0}' and '{1}'
    """.format(start.date().strftime("%Y-%m-%d"), end.date().strftime("%Y-%m-%d"))
    t = conn.update(sql)
    print '==========', t, start

#     print '----------', date
#     sql = """
#     update symbol_cons_300 a LEFT JOIN cons_300 b
# on a.symbol_id = b.symbol_id and DATE_FORMAT(a.dt, "%Y%m") = DATE_FORMAT(b.dt, "%Y%m")
# set a.weight = b.weight
# where a.dt = '{0}'
#     """.format(date.date().strftime("%Y-%m-%d"))
#     t = conn.update(sql)


# update symbol_cons_300 a LEFT JOIN (select symbol_id, weight from cons_300 where dt='2017-01-01') as b
# on a.symbol_id = b.symbol_id
# set a.weight = b.weight
# where a.dt betweent






