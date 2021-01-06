#  -*- coding: utf-8 -*-

from pymongo import UpdateOne
from database_self import DB_CONN
import tushare as ts
from datetime import datetime


class DailyCrawler:

    def __init__(self):
        # 创建daily数据集
        self.daily = DB_CONN['daily']
        # 创建daily_hfq数据集
        self.daily_hfq = DB_CONN['daily_hfq']


    # 抓取指数行情
    def crawl_index(self, begin_date=None, end_date=None):
        # 指定抓取的指数列表，可以增加和改变列表里的值
        index_codes = ['000001.SZ', '000300.SH', '000905.SH', '399001.SZ', '399005.SZ', '399006.SZ', '399016.SZ',
                       '399300.SZ']

        now = datetime.now().strftime('%Y-%m-%d')

        # 如果没有指定开始，则默认为当前日期
        if begin_date is None:
            begin_date = now

        # 如果没有指定结束日，则默认为当前日期
        if end_date is None:
            end_date = now

        # 按照指数的代码循环，抓取所有指数信息
        for code in index_codes:
            # 抓取一个指数的在时间区间的数据
            df_daily = ts.pro_api().daily(ts_code=code, start_date=begin_date, end_date=end_date)
            print(df_daily)
            # 保存数据
            self.save_data(code, df_daily, self.daily, {'index': True})

    # 抓取个股行情
    def crawl_company(self, begin_date=None, end_date=None):
        # 通过tushare的基本信息API，获取所有股票的基本信息
        stock_df = ts.pro_api().stock_basic()
        # 将基本信息的索引列表转化为股票代码列表
        codes = list(stock_df.ts_code)

        # 当前日期
        now = datetime.now().strftime('%Y-%m-%d')

        # 如果没有指定开始日期，则默认为当前日期
        if begin_date is None:
            begin_date = now

        # 如果没有指定结束日期，则默认为当前日期
        if end_date is None:
            end_date = now

        for code in codes:
            # 抓取不复权的价格
            # df_daily = ts.pro_api().daily(ts_code=code, start_date=begin_date, end_date=end_date)
            # self.save_data(code, df_daily, self.daily, {'index': False})
            # 抓取后复权的价格
            df_daily_hfq = ts.pro_bar(code, adj='hfq', start_date=begin_date, end_date=end_date)
            self.save_data(code, df_daily_hfq, self.daily_hfq, {'index': False})

    # 存储到数据库
    def save_data(self, code, df_daily, collection, extra_fields=None):
        # 数据更新的请求列表
        update_requests = []

        # 将DataFrame中的行情数据，生成更新数据的请求
        for df_index in df_daily.index:
            # 将DataFrame中的一行数据转dict
            doc = dict(df_daily.loc[df_index])
            # 设置股票代码
            doc['code'] = code

            # 如果指定了其他字段，则更新dict
            if extra_fields is not None:
                doc.update(extra_fields)

            # 生成一条数据库的更新请求
            # 注意：
            # 需要在code、date、index三个字段上增加索引，否则随着数据量的增加，
            # 写入速度会变慢，创建索引的命令式：
            # db.daily.createIndex({'code':1,'date':1,'index':1})
            update_requests.append(
                UpdateOne(
                    {'code': doc['ts_code'], 'date': doc['trade_date'], 'index': doc['index']},
                    {'$set': doc},
                    upsert=True)
            )

        # 如果写入的请求列表不为空，则保存都数据库中
        if len(update_requests) > 0:
            # 批量写入到数据库中，批量写入可以降低网络IO，提高速度
            update_result = collection.bulk_write(update_requests, ordered=False)
            print('保存日线数据，代码： %s, 插入：%4d条, 更新：%4d条' %
                  (code, update_result.upserted_count, update_result.modified_count),
                  flush=True)


if __name__ == '__main__':

    ts.set_token("47105aced0d886b2c9544eccf752c1b952eb109379a80def6119691f")
    dc = DailyCrawler()
    start_time = '20150101'
    end_time = '20160101'

    dc.crawl_index(start_time, end_time)
    dc.crawl_company(start_time, end_time)