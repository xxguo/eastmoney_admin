# -*- coding: utf-8 -*-
# @Time    : 4/4/20 6:42 AM
# @Author  : xxguo
# @Software: PyCharm
import time
import datetime
import pandas as pd
from db.mysql.connection import MysqlConnection


class AnanlysisData(object):
    def __init__(self):
        self.conn = MysqlConnection()

    def get_task_data(self):
        q_sql = "select  id, code, category_type from symbol_info where `status` = 2 and `a_status` = 0 order by crawl_level desc "
        try_count = 0
        while 1:
            try_count += 1
            result = self.conn.getOne(q_sql)
            if not result:
                sleep_len = try_count * 3 if try_count < 100 else 60 * 60
                print '--------task null,  try_count:{0}, now:{1}, sleep_time:{2}'.format(try_count, datetime.datetime.now(), sleep_len)
                time.sleep(sleep_len)
                continue
            break

        code = result['code']
        category_type = result['category_type']
        self.conn.update("update  symbol_info  set `a_status` = 1 where symbol_id = '{0}';".format(code))
        return code, category_type

    def get_group_by_result(self, code):
        q_sql = """
        select
	DATE_FORMAT(publish_time, '%Y-%m-%d') AS dt, count(1) total_count,
	SUM(case when a.score > 0.5 then 1 else 0 END) good_count,
	SUM(case when a.score >= 0.5 then (a.score - 0.5) * 2 * (a.like_count  + a.comment_count + a.forward_count)  else 0 END) good_a_score,
   SUM(case when a.score >= 0.5 then (a.score - 0.5) * 2 * a.click_count  else 0 END) good_b_score,
    SUM(case when a.score < 0.5 then (0.5 - a.score) * 2 * (a.like_count  + a.comment_count + a.forward_count) else 0 END) bad_a_score,
    SUM(case when a.score < 0.5 then (0.5 - a.score) * 2 * a.click_count else 0 END) bad_b_score
    from guba_info a where symbol_id={0} GROUP BY dt
        """.format(code)
        result = self.conn.getAll(q_sql)
        return result

    def _update_insert_data(self, data=None, data_list=None):
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
                insert_sql = "insert into guba_day_a_b_score ({0}) values ({1})".format(
                    ','.join(key_field), ','.join(['%s'] * key_len))
                _id = self.conn.insertOne(insert_sql, tuple(values_list))
                print 'new insert----- _id', _id
        elif data_list:
            first_data = data_list[0]
            symbol_id = first_data['symbol_id']

            del_count = self.conn.delete("DELETE FROM guba_day_a_b_score where symbol_id = {0};".format(symbol_id))
            print "del ----{0} count: {1}".format(symbol_id, del_count)
            key_field = first_data.keys()
            key_len = len(key_field)
            insert_sql = "insert into guba_day_a_b_score ({0}) values ({1})".format(
                ','.join(key_field), ','.join(['%s'] * key_len))

            values_list = []
            for data in data_list:
                values_list.append(data.values())
            insert_count = self.conn.insertMany(insert_sql, values_list)
            print "insert =============== {0} count: {1}, {2}".format(symbol_id, insert_count, len(data_list))
            del data_list

    def update_symbol_info_data(self, symbol_id):
        try:
            result = self.conn.getOne("select count(1) t, min(publish_time) publish_time, min(last_time) last_time from guba_info where symbol_id={0} and last_time > '20001-01-01';".format(symbol_id))
            print '--------', symbol_id, result
            sql = "update symbol_info set crawl_count = {0}, min_publish_time= '{1}', min_last_time = '{2}' where symbol_id={3};".format(
                result['t'], result['publish_time'], result['last_time'], symbol_id
            )
            pdate_count = self.conn.update(sql)
            print '执行结果---------', pdate_count
        except:
            import traceback
            print "error-----------------"
            print traceback.format_exc()


    def run(self):

        # self.ananlysis_data(688366)
        while 1:
            code, category_type = self.get_task_data()
            print 'start running --------code ', code
            try:
                self.update_symbol_info_data(code)
                self.ananlysis_data(code, category_type=category_type)
                self.conn.update("update  symbol_info  set `a_status` = 2 where symbol_id = '{0}'".format(code))
            except Exception as e:
                self.conn.update("update  symbol_info  set `a_status` = 3 where symbol_id = '{0}'".format(code))
                import traceback
                print traceback.format_exc()
                continue

    def ananlysis_data(self, code, category_type=0):
        result = list(self.get_group_by_result(code))
        start_date = result[0]["dt"]
        end_date = result[-1]["dt"]
        df = pd.DataFrame(result)
        df.set_index('dt', inplace=True)
        df['total_count'] = df['total_count'].astype('int')
        df['good_count'] = df['good_count'].astype('int')
        df['good_a_score'] = df['good_a_score'].astype('float')
        df['good_b_score'] = df['good_b_score'].astype('float')
        df['bad_a_score'] = df['bad_a_score'].astype('float')
        df['bad_b_score'] = df['bad_b_score'].astype('float')
        df_date = pd.DataFrame(pd.date_range(start_date, end_date, freq='D'), columns=['dt'])
        df_date.set_index('dt', inplace=True)
        df = df.merge(df_date, how='right', left_index=True, right_index=True)
        columns_list = ['total_count', 'good_count', 'good_a_score', 'good_b_score', 'bad_a_score', 'bad_b_score']
        df[['good_a_score', 'good_b_score', 'bad_a_score', 'bad_b_score']].astype(float)
        df[map(lambda x: x + '_7', columns_list)] = df[columns_list].rolling(7, min_periods=1, axis=0).sum()
        df[map(lambda x: x + '_30', columns_list)] = df[columns_list].rolling(30, min_periods=1, axis=0).sum()
        df.fillna(0, inplace=True)
        data_list = []
        for index, row in df.iterrows():
            item = row.to_dict()
            data = {
                "dt": str(index.date()),
                "symbol_id": code,
                "code": code,
                "category_type": category_type,
                "total_count": item["total_count"],
                "good_count": item["good_count"],
                "bad_count": item["total_count"] - item["good_count"],
                "good_a_score": item["good_a_score"],
                "good_b_score": item["good_b_score"],
                "bad_a_score": item["bad_a_score"],
                "bad_b_score": item["bad_b_score"],

                "total_count_7": item["total_count_7"],
                "good_count_7": item["good_count_7"],
                "bad_count_7": item["total_count_7"] - item["good_count_7"],
                "good_a_score_7": item["good_a_score_7"],
                "good_b_score_7": item["good_b_score_7"],
                "bad_a_score_7": item["bad_a_score_7"],
                "bad_b_score_7": item["bad_b_score_7"],

                "total_count_30": item["total_count_30"],
                "good_count_30": item["good_count_30"],
                "bad_count_30": item["total_count_30"] - item["good_count_30"],
                "good_a_score_30": item["good_a_score_30"],
                "good_b_score_30": item["good_b_score_30"],
                "bad_a_score_30": item["bad_a_score_30"],
                "bad_b_score_30": item["bad_b_score_30"],
            }

            data_list.append(data)

        self._update_insert_data(data_list=data_list)

