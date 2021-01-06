#  -*- coding: utf-8 -*-

"""
普量学院量化投资课程系列案例源码包
普量学院版权所有
仅用于教学目的，严禁转发和用于盈利目的，违者必究
©Plouto-Quants All Rights Reserved

普量学院助教微信：niuxiaomi3
"""

"""
compute_pe：计算市盈率
"""

from pymongo import DESCENDING, UpdateOne

from database_self import DB_CONN
from stock_util_self import get_all_codes

finance_report_collection = DB_CONN['finance_report']
daily_collection = DB_CONN['daily']


def compute_pe():
    """
    计算股票在某只的市盈率
    """

    # 获取所有股票
    codes = get_all_codes()

    for code in codes:
        print('计算市盈率, %s' % code)
        daily_cursor = daily_collection.find(
            {'code': code},
            projection={'close': True, 'date': True})

        update_requests = []
        for daily in daily_cursor:
            _date = daily['date']
            _code = code[0:6]
            # 找到该股票距离当前日期最近的年报，通过公告日期查询，防止未来函数
            finance_report = finance_report_collection.find_one(
                {'code': _code, 'report_date': {'$regex': '\d{4}-12-31'}, 'announced_date': {'$lte': _date}},
                sort=[('announced_date', DESCENDING)]
            )

            if finance_report is None:
                continue

            # 计算滚动市盈率并保存到daily_k中
            eps = 0
            if finance_report['eps'] != '-':
                eps = finance_report['eps']

            # 计算PE
            if eps != 0:
                try:
                    update_result = daily_collection.update_one({'code': code, 'date': _date},
                                                            {'$set': {'pe': round(daily['close'] / eps)}}, True)
                    print('111111111更新PE, %s, 更新：%d' % (code, update_result.modified_count))
                except Exception as e:
                    print(code+"______"+_date)


if __name__ == "__main__":
    compute_pe()
