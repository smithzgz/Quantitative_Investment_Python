import tushare as ts
import pandas as pd
import MySQLdb
import pymysql

from sqlalchemy import create_engine


class Baisc():

    def init_tushare(self):
        pro = ts.pro_api()
        token = "47105aced0d886b2c9544eccf752c1b952eb109379a80def6119691f"
        ts.set_token(token)
        return pro

    def read_tushare_data(self):
        pro = self.init_tushare()
        df_moneyflow = pro.stk_holdernumber(ts_code='601318.SH', start_date='20000101', end_date='20211231')
        print(df_moneyflow)

    def init_db(self):
        engine = create_engine('mysql+pymysql://root:123456@localhost:3306/quant')
        db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="quant", charset="utf8")
        cursor = db.cursor()
        # result = pd.read_sql_query('select DISTINCT Name from city ', engine)
        # print(result)
        return db, cursor

    def show_data(self):
        pass


if __name__ == "__main__":
    a = Baisc()
    a.read_tushare_data()
    a.init_db()
