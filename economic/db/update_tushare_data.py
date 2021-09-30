import time
import MySQLdb
import tushare_test as ts
from constants_table import Constants
from generate_sql import GenerateSql
from init_tushare_data import InitTushareData


class UpdateTushareData():

    def update_daily_table(self, db):
        cursor = db.cursor()
        pro = ts.pro_api()
        # 查询当前所有正常上市交易的股票列表
        stock_basic_data = pro.stock_basic(exchange='', fields='ts_code')
        for ts_code in stock_basic_data["ts_code"]:
            sql = GenerateSql.generate_latest_date_sql(GenerateSql, "daily", "trade_date", ts_code)
            cursor.execute(sql)
            latest_date = cursor.fetchall()
            latest_date_string = latest_date[0][0].strftime("%Y%m%d")
            print(ts_code, " latest_date_string: ", latest_date_string)

            daily_data = pro.daily(ts_code=ts_code, start_date=latest_date_string, end_date='20200101')
            InitTushareData.common_insert(InitTushareData, db, "daily", Constants.daily, daily_data)
            print(ts_code, "---update success!")
            time.sleep(0.5)

if __name__ == '__main__':
    updateTushareData = UpdateTushareData();

    db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="daily data", charset="utf8")
    updateTushareData.update_daily_table(db)
    print("---update complete!")