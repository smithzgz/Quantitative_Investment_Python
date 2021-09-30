import sys
import MySQLdb
import time
import tushare_test as ts
from constants_table import Constants
from generate_sql import GenerateSql
import pandas as pd
import numpy as np


class InitTushareData():
    # 创建新表
    def crate_table(self, db, table_name, field_name_list):
        cursor = db.cursor()
        try:
            if cursor.execute(GenerateSql.generate_check_table_exist_sql(self, table_name)) == 0:
                cursor.execute(GenerateSql.generate_crate_table_sql(self, table_name, field_name_list))
                db.commit()
                print("success crate table : ", table_name)
            else:
                return
                # print("failed crate table : table exist ", table_name)
        except Exception as e:
            print("------failed crate table catch exception ", e)
        else:
            print("crate_table done ", table_name)

    # 创建新表 并删除旧表
    def crate_table_with_delete(self, db, table_name, field_name_list):
        cursor = db.cursor()
        try:
            if cursor.execute(GenerateSql.generate_check_table_exist_sql(self, table_name)) == 1:
                cursor.execute(GenerateSql.generate_delete_table_sql(self, table_name))
                db.commit()
                print("table exist : delete success!", table_name)
            cursor.execute(GenerateSql.generate_crate_table_sql(self, table_name, field_name_list))
            db.commit()
        except Exception as e:
            print("------failed crate table catch exception ", e)
        else:
            print("crate_table_with_delete done ", table_name)

    # 向信标插入数据
    def common_insert(self, db, table_name, field_name_list, data_list):
        cursor = db.cursor()
        self.crate_table(db, table_name, field_name_list)

        count = 0;
        sql_list = GenerateSql.generate_common_insert_sql(self, table_name, field_name_list, data_list)
        for sql in sql_list:
            try:
                cursor.execute(sql)
                db.commit()
                count = count + 1;
            except Exception as e:
                print(sql)
                print("------failed insert table catch exception ", e)
            # else:
            # print("success insert ", table_name, count, " times")

    def update_stock_basic_data(self, db, pro):
        stock_basic_data = pro.stock_basic(exchange='',
                                           fields='ts_code,symbol,name,area,industry,fullname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
        initTushareData.common_insert(db, "stock_basic", Constants.stock_basic, stock_basic_data)
        print("stock_basic_data-------------------complete")

    def update_trade_cal_data(self, db, pro, end_date):
        trade_cal_data = pro.trade_cal(exchange='', start_date='19900101', end_date=end_date)
        initTushareData.common_insert(db, "trade_cal", Constants.trade_cal, trade_cal_data)
        print("trade_cal_data-------------------complete")

    def update_trade_daily_data(self, db, pro, start_date, end_date):
        trade_cal_data = pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
        for date_index in trade_cal_data.index:
            # 获取股票基本信息，包括 PE、PB 值
            cal_date = trade_cal_data.cal_date[date_index];
            is_open = trade_cal_data.is_open[date_index];
            if (is_open == 1):
                # 股票基本数据
                df_base = pro.daily_basic(ts_code='', trade_date=cal_date)
                # 获取股票当天数据，包括当前股价
                df_todays = pro.daily(trade_date=cal_date)
                # 获得复权因子
                df_adj_factor = pro.adj_factor(ts_code='', trade_date=cal_date)
                # 获取个股资金流向
                df_moneyflow = pro.moneyflow(trade_date=cal_date)

                # 整合股价与 PE、PB 数据
                daily_data = pd.merge(df_base, df_todays, how='right', on=['ts_code', 'close'])
                # 整合复权因子
                daily_data = pd.merge(df_adj_factor, daily_data, how='right', on=['ts_code'])
                # 整合资金流向
                daily_data = pd.merge(df_moneyflow, daily_data, how='right', on=['ts_code'])

                daily_data["trade_date"] = np.array([cal_date] * daily_data["ts_code"].size)

                initTushareData.common_insert(db, "daily", Constants.daily, daily_data)
                print(cal_date, "--------success!")
                # time.sleep(0.2)
        print("daily_data-------------------complete")

    def update_hs_const_data(self, db, pro):
        hs_const_sh = pro.hs_const(hs_type='SH')
        initTushareData.common_insert(db, "hs_const", Constants.hs_const, hs_const_sh)
        hs_const_sz = pro.hs_const(hs_type='SZ')
        initTushareData.common_insert(db, "hs_const", Constants.hs_const, hs_const_sz)
        print("hs_const-------------------complete")

    def update_namechange_data(self, db, pro):
        namechange_data = pro.namechange(fields='ts_code,name,start_date,end_date,ann_date,change_reason')
        initTushareData.common_insert(db, "namechange", Constants.namechange, namechange_data)
        print("namechange_data-------------------complete")

    def update_financial_data(self, db, pro, start_date, end_date):
        offset = 100000  # 以10年为周期
        stock_basic_data = pro.stock_basic(exchange='',
                                           fields='ts_code,symbol,name,area,industry,fullname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
        for ts_code in stock_basic_data["ts_code"]:
            date_array = np.arange(int(start_date), int(end_date), offset)
            date_array = np.append(date_array, int(end_date))
            for i in range(date_array.size - 1):
                # 利润表
                income = pro.income(ts_code=ts_code, start_date=str(date_array[i]), end_date=str(date_array[i + 1]))
                initTushareData.common_insert(db, "income", Constants.income, income)
                # 资产负债表
                balancesheet = pro.balancesheet(ts_code=ts_code, start_date=str(date_array[i]),
                                                end_date=str(date_array[i + 1]))
                initTushareData.common_insert(db, "balancesheet", Constants.balancesheet, balancesheet)
                # 现金流量表
                cashflow = pro.cashflow(ts_code=ts_code, start_date=str(date_array[i]), end_date=str(date_array[i + 1]))
                initTushareData.common_insert(db, "cashflow", Constants.cashflow, cashflow)
                # 分红送股
                dividend = pro.dividend(ts_code=ts_code, start_date=str(date_array[i]), end_date=str(date_array[i + 1]))
                initTushareData.common_insert(db, "dividend", Constants.dividend, dividend)
                # 财务指标数据
                fina_indicator = pro.fina_indicator(ts_code=ts_code, start_date=str(date_array[i]),
                                                    end_date=str(date_array[i + 1]))
                initTushareData.common_insert(db, "fina_indicator", Constants.fina_indicator, fina_indicator)
                # 财务审计意见
                fina_audit = pro.fina_audit(ts_code=ts_code, start_date=str(date_array[i]),
                                            end_date=str(date_array[i + 1]))
                initTushareData.common_insert(db, "fina_audit", Constants.fina_audit, fina_audit)
                # 主营业务构成
                fina_mainbz = pro.fina_mainbz(ts_code=ts_code, start_date=str(date_array[i]),
                                              end_date=str(date_array[i + 1]))
                initTushareData.common_insert(db, "fina_mainbz", Constants.fina_mainbz, fina_mainbz)
                time.sleep(1)
            print(ts_code, "--------success!")
        print("financial_data-------------------complete")

    def update_index_basic_data(self, db, pro, start_date, end_date):
        offset = 50000  # 以5年为周期
        markets = ["CSI", "SSE", "SZSE", "CICC", "SW", "CNI", "OTH"]
        initTushareData.crate_table_with_delete(db, "index_basic", Constants.index_basic)
        for market in markets:
            # 指数基本信息
            index_basic = pro.index_basic(market=market)
            initTushareData.common_insert(db, "index_basic", Constants.index_basic, index_basic)

            for index_code in index_basic['ts_code']:
                date_array = np.arange(int(start_date), int(end_date), offset)
                date_array = np.append(date_array, int(end_date))
                for i in range(date_array.size - 1):
                    # 指数日线
                    index_daily = pro.index_daily(ts_code=index_code, start_date=str(date_array[i]),
                                                  end_date=str(date_array[i + 1]))
                    initTushareData.common_insert(db, "index_daily", Constants.index_daily, index_daily)
                    # 指数权重信息
                    index_weight = pro.index_weight(index_code=index_code, start_date=str(date_array[i]),
                                                    end_date=str(date_array[i + 1]))
                    initTushareData.common_insert(db, "index_weight", Constants.index_weight, index_weight)
                    time.sleep(2)
                    print(index_code, "--------success!")
        print("index_basic_data-------------------complete")

    def update_index_dailybasic_data(self, db, pro, start_date, end_date):
        offset = 50000  # 以5年为周期
        index_codes = ['000001.SH', '000300.SH', '000905.SH', '399001.SZ', '399005.SZ', '399006.SZ', '399016.SZ',
                       '399300.SZ']
        for index_code in index_codes:
            date_array = np.arange(int(start_date), int(end_date), offset)
            date_array = np.append(date_array, int(end_date))
            for i in range(date_array.size - 1):
                index_dailybasic = pro.index_dailybasic(ts_code=index_code, start_date=str(date_array[i]),
                                                        end_date=str(date_array[i + 1]))
                initTushareData.common_insert(db, "index_dailybasic", Constants.index_dailybasic, index_dailybasic)
                time.sleep(1)
            print('-------------指数------------', index_code, "--------success!")
        print("index_dailybasic_data-------------------complete")

    def update_fund_data(self, db, pro):
        # 公募基金基本信息
        fund_basic = pro.fund_basic()
        initTushareData.common_insert(db, "fund_basic", Constants.fund_basic, fund_basic)
        for ts_code in fund_basic["ts_code"]:
            # 公募基金净值
            fund_nav = pro.fund_nav(ts_code=ts_code)
            initTushareData.common_insert(db, "fund_nav", Constants.fund_nav, fund_nav)
            # 公募基金分红
            fund_div = pro.fund_div(ts_code=ts_code)
            initTushareData.common_insert(db, "fund_div", Constants.fund_div, fund_div)
            print('-------------公募基金------------', ts_code, "--------success!")
            time.sleep(1)
        print("fund_data-------------------complete")

    def update_rate_index_data(self, db, pro, start_date, end_date):
        offset = 50000  # 以5年为周期
        date_array = np.arange(int(start_date), int(end_date), offset)
        date_array = np.append(date_array, int(end_date))
        for i in range(date_array.size - 1):
            shibor = pro.shibor(start_date=str(date_array[i]), end_date=str(date_array[i + 1]))
            initTushareData.common_insert(db, "shibor", Constants.shibor, shibor)

            shibor_lpr = pro.shibor_lpr(start_date=str(date_array[i]), end_date=str(date_array[i + 1]))
            initTushareData.common_insert(db, "shibor_lpr", Constants.shibor_lpr, shibor_lpr)

            libor = pro.libor(start_date=str(date_array[i]), end_date=str(date_array[i + 1]))
            initTushareData.common_insert(db, "libor", Constants.libor, libor)

            hibor = pro.hibor(start_date=str(date_array[i]), end_date=str(date_array[i + 1]))
            initTushareData.common_insert(db, "hibor", Constants.hibor, hibor)

            time.sleep(10)
            print('-------------time_ranges------------', str(date_array[i]), str(date_array[i + 1]),
                  "--------success!")
        print("rate_index_data-------------------complete")


if __name__ == '__main__':
    initTushareData = InitTushareData()
    db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="daily data", charset="utf8")
    pro = ts.pro_api()
    start_date = '19910101'
    end_date = '20190817'

    # 股票列表 查询当前所有正常上市交易的股票列表
    # initTushareData.update_stock_basic_data(db, pro)

    # 交易日历
    # initTushareData.update_trade_cal_data(db, pro, end_date)

    # 日线行情
    # initTushareData.update_trade_daily_data(db, pro, start_date, end_date)

    # 沪深股通成份股
    # initTushareData.update_hs_const_data(db, pro)

    # 股票曾用名
    # initTushareData.update_namechange_data(db, pro)

    # ------------- 财务报表 -------------
    # 利润表\资产负债表\现金流量表\分红送股\财务指标数据\财务审计意见\主营业务构成
    # initTushareData.update_financial_data(db, pro, start_date, end_date)

    # -------------指数------------
    # 指数基本信息、日线、权重
    initTushareData.update_index_basic_data(db, pro, start_date, end_date)

    # 大盘指数每日指标
    # initTushareData.update_index_dailybasic_data(db, pro, start_date, end_date)

    # # -------------公募基金------------
    # initTushareData.update_fund_data(db, pro)

    # # -------------利率数据------------
    # initTushareData.update_rate_index_data(db, pro, start_date, end_date)

    sys.exit(0)
# updateTushareDate.crate_table_with_delete(db, "trade_cal", Constants.trade_cal)
# updateTushareDate.common_insert(db, "trade_cal", Constants.trade_cal, [['s3h', '20180101', '1', '20180101'],['s3h2', '20180101', '1', '20180101'],['s3h1', '20180101', '1', '20180101']])
# db.close()
