# -*- coding: utf-8 -*-
# @Time    : 4/10/20 8:51 PM
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
# trade_date = conn.getAll("select dt from trading_days ")
# date_list = map(lambda x: str(x["dt"]), trade_date)
# print date_list
#
# update_count = conn.update("update guba_day_score set is_trad_date=1 where dt in {0};".format(str(tuple(date_list))))
#
# print "data------", update_count


def insert_cons_info(data_list):
    first_data = data_list[0]
    key_field = first_data.keys()
    key_len = len(key_field)
    insert_sql = "insert into symbol_cons_1000 ({0}) values ({1})".format(
                ','.join(key_field), ','.join(['%s'] * key_len))
    values_list = []
    for data in data_list:
        values_list.append(data.values())
    insert_count = conn.insertMany(insert_sql, values_list)
    print "insert =============== {0} count: {1}, {2}".format('00', insert_count, len(data_list))

result = conn.getAll("select * from tmp_cons_1000 ORDER BY dt")
start_date = result[0]["dt"]
date_list = pd.date_range(start_date, '2020-04-11', freq='D').to_list()

last_date = ''
last_symbol_set = set([])
symb_info_dict = dict()
# date_symb_info = {}
trade_list = []
symbol_list = []
for item in result:
    cur_symbol_id = item['symbol_id']
    symb_info_dict.setdefault(cur_symbol_id, {"symbol_id": cur_symbol_id,
                                              "code": item['code'],
                                              "code_name": item['code_name']})
    cur_date = item['dt']
    cur_t_type = item['t_type']
    if cur_date != last_date:
        if last_symbol_set:
            trade_list.append(last_date)
            symbol_list.append(deepcopy(last_symbol_set))
        last_date = cur_date
    else:
        pass
    if cur_t_type == u"剔除":
        last_symbol_set -= set([cur_symbol_id])
        print 'del -------', cur_symbol_id, cur_date, len(last_symbol_set)
    elif cur_t_type == u"纳入":
        last_symbol_set |= set([cur_symbol_id])
        print 'add ++++++', cur_symbol_id, cur_date, len(last_symbol_set)
    else:
        print '=========', cur_t_type
        print item
        raise ValueError(cur_t_type)

trade_list.append(last_date)
symbol_list.append(last_symbol_set)
df = pd.DataFrame({'dt': trade_list, 'data': symbol_list}, columns=['dt', 'data'])
df.set_index('dt', inplace=True)
df_date = pd.DataFrame(pd.date_range('2014-10-01', '2020-04-11', freq='D'), columns=['dt'])
df_date.set_index('dt', inplace=True)
df = df.merge(df_date, how='right', left_index=True, right_index=True)
df.fillna(method='ffill', inplace=True)

df = df.loc['2016-10-01': '2020-04-11']

for index, row in df.iterrows():
    data_list = []
    for symbol_id in row.to_dict()['data']:
        item = symb_info_dict[symbol_id]
        data = {
            "dt": str(index),
            "symbol_id": symbol_id,
            "code": item["code"],
            "code_name": item["code_name"],
            "category_type": 1,
        }
        data_list.append(data)
    insert_cons_info(data_list)

a = 1

conn.colse()

