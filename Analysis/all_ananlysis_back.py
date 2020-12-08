# -*- coding: utf-8 -*-
# @Time    : 4/10/20 8:20 PM
# @Author  : xxguo
# @Software: PyCharm


import pandas as pd
from db.mysql.connection import MysqlConnection


class AnanlysisCategoryData(object):
    def __init__(self):
        self.conn = MysqlConnection()

    def get_task_data(self):
        q_sql = "select  id, code, category_type from symbol_info where `status` = 2 and `a_status` = 0 order by crawl_level desc "
        result = self.conn.getOne(q_sql)
        if not result:
            print '=======没shu ju l end+++======'
        code = result['code']
        category_type = result['category_type']
        self.conn.update("update  symbol_info  set `a_status` = 1 where symbol_id = '{0}';".format(code))
        return code, category_type

    def get_group_by_result(self, code_list=None):
        if code_list:
            pass
        else:
            # yiyao, 300, 500
            sql = """
             select a.dt,
                SUM(a.total_count) as total_count,
              SUM(a.good_count) as good_count,
              SUM(a.good_score) as good_score,
                SUM(a.bad_score) as bad_score
            from guba_day_score a
                join
             symbol_cons_1000 b
            on a.dt = b.dt and a.symbol_id = b.symbol_id
        where a.is_trad_date=1 and a.dt>='2016-12-01' GROUP BY a.dt
            """

            # all
    #         sql = """
    #         select dt,
    #     SUM(total_count) as total_count,
    #   SUM(good_count) as good_count,
    #   SUM(good_score) as good_score,
    #     SUM(bad_score) as bad_score
    # from guba_day_score where is_trad_date=1 and dt>='2016-12-01' GROUP BY dt
    #         """
            result = self.conn.getAll(sql)
        return result

    def _update_insert_data(self, data=None, data_list=None, category_type=0):
        if data:
            dt = data['dt']
            symbol_id = data['symbol_id']
            q_sql = "select id from guba_day_score where dt='{0}' and symbol_id = {1};".format(dt, symbol_id)
            is_exist = self.conn.getOne(q_sql)
            if is_exist:
                id = is_exist['id']
                data.pop("dt")
                data.pop("symbol_id")
                data.pop("code", None)
                key_field = data.keys()
                values_list = data.values()
                data_str = ','.join(map(lambda x: x + '= %s', key_field))
                update_sql = "update guba_day_score set {0} where id={1};".format(data_str, id)
                _id = self.conn.update(update_sql, values_list)
                print 'old update----- _id:{0}, count:{1}'.format(id, _id)
            else:
                key_field = data.keys()
                key_len = len(key_field)
                values_list = data.values()
                insert_sql = "insert into guba_day_score ({0}) values ({1})".format(
                    ','.join(key_field), ','.join(['%s'] * key_len))
                _id = self.conn.insertOne(insert_sql, tuple(values_list))
                print 'new insert----- _id', _id
        elif data_list:
            first_data = data_list[0]

            del_count = self.conn.delete("DELETE FROM guba_trading_category_score where category_type = {0};".format(category_type))
            print "del ----{0} count: {1}".format(category_type, del_count)
            key_field = first_data.keys()
            key_len = len(key_field)
            insert_sql = "insert into guba_trading_category_score ({0}) values ({1})".format(
                ','.join(key_field), ','.join(['%s'] * key_len))

            values_list = []
            for data in data_list:
                values_list.append(data.values())
            insert_count = self.conn.insertMany(insert_sql, values_list)
            print "insert =============== {0} count: {1}, {2}".format(category_type, insert_count, len(data_list))
            del data_list

    def run(self):

        self.ananlysis_data()
        # while 1:
        #     code, category_type = self.get_task_data()
        #     print 'start running --------code ', code
        #     try:
        #         self.ananlysis_data(code, category_type=category_type)
        #         self.conn.update("update  symbol_info  set `a_status` = 2 where symbol_id = '{0}'".format(code))
        #     except Exception as e:
        #         self.conn.update("update  symbol_info  set `a_status` = 3 where symbol_id = '{0}'".format(code))
        #         import traceback
        #         print traceback.format_exc()
        #         continue

    def ananlysis_data(self, code=None, category_type=1000):
        result = list(self.get_group_by_result(code))

        df = pd.DataFrame(result)
        df.set_index('dt', inplace=True)
        df['total_count'] = df['total_count'].astype('int')
        df['good_count'] = df['good_count'].astype('int')
        df['good_score'] = df['good_score'].astype('float')
        df['bad_score'] = df['bad_score'].astype('float')
        columns_list = ['total_count', 'good_count', 'good_score', 'bad_score']
        df[['good_score', 'bad_score']].astype(float)
        df[map(lambda x: x + '_5', columns_list)] = df[columns_list].rolling(5, min_periods=1, axis=0).sum()
        df[map(lambda x: x + '_20', columns_list)] = df[columns_list].rolling(20, min_periods=1, axis=0).sum()
        df.fillna(0, inplace=True)
        data_list = []
        for index, row in df.iterrows():
            item = row.to_dict()
            data = {
                "dt": str(index),
                # "symbol_id": code,
                # "code": code,
                "category_type": 1000,
                "total_count": item["total_count"],
                "good_count": item["good_count"],
                "bad_count": item["total_count"] - item["good_count"],
                "good_score": item["good_score"],
                "bad_score": item["bad_score"],

                "total_count_5": item["total_count_5"],
                "good_count_5": item["good_count_5"],
                "bad_count_5": item["total_count_5"] - item["good_count_5"],
                "good_score_5": item["good_score_5"],
                "bad_score_5": item["bad_score_5"],

                "total_count_20": item["total_count_20"],
                "good_count_20": item["good_count_20"],
                "bad_count_20": item["total_count_20"] - item["good_count_20"],
                "good_score_20": item["good_score_20"],
                "bad_score_20": item["bad_score_20"],
            }

            data_list.append(data)

        self._update_insert_data(data_list=data_list, category_type=category_type)


if __name__ == '__main__':
    AnanlysisCategoryData().run()
