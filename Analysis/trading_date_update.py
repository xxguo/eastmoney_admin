# -*- coding: utf-8 -*-
# @Time    : 4/14/20 6:52 AM
# @Author  : xxguo
# @Software: PyCharm
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import operator
import pandas as pd
from copy import deepcopy
from db.mysql.connection import MysqlConnection

conn = MysqlConnection()
trade_date = conn.getAll("select dt from trading_days ")
date_list = map(lambda x: str(x["dt"]), trade_date)
print date_list

for date in date_list:
    update_count = conn.update("update guba_day_a_b_score set is_trad_date=1 where dt= '{0}' and is_trad_date =0 ;".format(date))

    print "data------", update_count, date


conn.colse()
