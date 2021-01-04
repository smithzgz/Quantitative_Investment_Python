#  -*- coding: utf-8 -*-

from pymongo import ASCENDING
from database_self import DB_CONN
from datetime import datetime, timedelta


def get_trading_dates(begin_date=None, end_date=None):
    now = datetime.now()

    if begin_date is None:
        one_year_ago = now - timedelta(days=365)
        # 转化为str类型
        begin_date = one_year_ago.strftime('%Y-%m-%d')

    # 结束日期默认为今天
    if end_date is None:
        end_date = now.strftime('%Y-%m-%d')

    # 用上证综指000001作为查询条件，因为指数是不会停牌的，所以可以查询到所有的交易日
    daily_cursor = DB_CONN.daily.find(
        {'code': '000001.SZ', 'date': {'$gte': begin_date, '$lte': end_date}, 'index': True},
        sort=[('date', ASCENDING)],
        projection={'date': True, '_id': False})

    # 转换为日期列表
    dates = [x['date'] for x in daily_cursor]
    return dates


def get_all_codes():
    # 通过distinct函数拿到所有不重复的股票代码列表
    return DB_CONN.daily.distinct('code')


if __name__ == '__main__':
    print(get_all_codes())
    print(get_trading_dates())
