# -*- coding: utf-8 -*-
# @Time    : 4/10/20 8:20 PM
# @Author  : xxguo
# @Software: PyCharm


import pandas as pd
from db.mysql.connection import MysqlConnection


class AnanlysisCategoryData(object):
    def __init__(self):
        self.conn = MysqlConnection()

    def get_group_by_result(self, code_list=None):
        print "type -------------", self._type
        if code_list:
            pass
        else:
            # yiyao, 300, 500

            if self._type == 'A':
                sql = """
                        select dt,
                    SUM(total_count) as total_count,
                  SUM(good_count) as good_count,
                  SUM(good_a_score) as good_a_score,
                  SUM(good_b_score) as good_b_score,
                    SUM(bad_a_score) as bad_a_score,
                    SUM(bad_b_score) as bad_b_score
                from guba_day_a_b_score where is_trad_date=1 and dt>='2016-12-01' GROUP BY dt
                        """
            elif self._type != 'yiyao' and self.is_weight:
                sql = """
                        select a.dt,
                        SUM(a.total_count) as total_count,
                      SUM(a.good_count) as good_count,
                      SUM(a.good_a_score * b.weight) as good_a_score,
                      SUM(a.good_b_score * b.weight) as good_b_score,
                        SUM(a.bad_a_score * b.weight) as bad_a_score,
                        SUM(a.bad_b_score * b.weight) as bad_b_score
                    from guba_day_a_b_score a
                        join
                     symbol_cons_{0} b
                    on a.dt = b.dt and a.symbol_id = b.symbol_id
                where a.is_trad_date=1 and a.dt>='2016-12-01' GROUP BY a.dt;
                """.format(self._type)
            else:
                sql = """
                 select a.dt,
                    SUM(a.total_count) as total_count,
                  SUM(a.good_count) as good_count,
                  SUM(a.good_a_score) as good_a_score,
                  SUM(a.good_b_score) as good_b_score,
                    SUM(a.bad_a_score) as bad_a_score,
                    SUM(a.bad_b_score) as bad_b_score
                from guba_day_a_b_score a
                    join
                 symbol_cons_{0} b
                on a.dt = b.dt and a.symbol_id = b.symbol_id
            where a.is_trad_date=1 and a.dt>='2016-12-01' GROUP BY a.dt
                """.format(self._type)


            # all

            result = self.conn.getAll(sql)
        return result

    def _update_insert_data(self, data=None, data_list=None, category_type=0):
        if data:
            pass
        elif data_list:
            first_data = data_list[0]

            del_count = self.conn.delete("DELETE FROM guba_ab_trading_category_score where category_type = {0};".format(category_type))
            print "del ----{0} count: {1}".format(category_type, del_count)
            key_field = first_data.keys()
            key_len = len(key_field)
            insert_sql = "insert into guba_ab_trading_category_score ({0}) values ({1})".format(
                ','.join(key_field), ','.join(['%s'] * key_len))

            values_list = []
            for data in data_list:
                values_list.append(data.values())
            insert_count = self.conn.insertMany(insert_sql, values_list)
            print "insert =============== {0} count: {1}, {2}".format(category_type, insert_count, len(data_list))
            del data_list

    def run(self, _type, is_weight=True):
        if _type not in  ('A', 'yiyao', 300, 500, 1000):
            raise ValueError("值错误")

        self._type =_type
        self.is_weight = is_weight
        self.ananlysis_data()

    def ananlysis_data(self, code=None):

        if self._type == 'yiyao':
            category_type = 1
        elif self._type == 'A':
            category_type = 0
        else:
            category_type = self._type
        result = list(self.get_group_by_result(code))

        df = pd.DataFrame(result)
        df.set_index('dt', inplace=True)
        df['total_count'] = df['total_count'].astype('int')
        df['good_count'] = df['good_count'].astype('int')
        df['good_a_score'] = df['good_a_score'].astype('float')
        df['good_b_score'] = df['good_b_score'].astype('float')
        df['bad_a_score'] = df['bad_a_score'].astype('float')
        df['bad_b_score'] = df['bad_b_score'].astype('float')
        columns_list = ['total_count', 'good_count', 'good_a_score', 'good_b_score', 'bad_a_score', 'bad_b_score']
        df[['good_a_score', 'good_b_score', 'bad_a_score', 'bad_b_score']].astype(float)
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
                "category_type": category_type,
                "total_count": item["total_count"],
                "good_count": item["good_count"],
                "bad_count": item["total_count"] - item["good_count"],
                 "good_a_score": item["good_a_score"],
                "good_b_score": item["good_b_score"],
                "bad_a_score": item["bad_a_score"],
                "bad_b_score": item["bad_b_score"],

               "total_count_5": item["total_count_5"],
                "good_count_5": item["good_count_5"],
                "bad_count_5": item["total_count_5"] - item["good_count_5"],
                "good_a_score_5": item["good_a_score_5"],
                "good_b_score_5": item["good_b_score_5"],
                "bad_a_score_5": item["bad_a_score_5"],
                "bad_b_score_5": item["bad_b_score_5"],

                "total_count_20": item["total_count_20"],
                "good_count_20": item["good_count_20"],
                "bad_count_20": item["total_count_20"] - item["good_count_20"],
                "good_a_score_20": item["good_a_score_20"],
                "good_b_score_20": item["good_b_score_20"],
                "bad_a_score_20": item["bad_a_score_20"],
                "bad_b_score_20": item["bad_b_score_20"],
            }

            data_list.append(data)

        self._update_insert_data(data_list=data_list, category_type=category_type)


if __name__ == '__main__':
    # AnanlysisCategoryData().run(_type='A')
    # AnanlysisCategoryData().run(_type='yiyao')
    AnanlysisCategoryData().run(_type=300)
    # AnanlysisCategoryData().run(_type=300, is_weight=False)
