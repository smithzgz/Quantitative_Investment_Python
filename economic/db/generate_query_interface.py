import MySQLdb
import pandas as pd
from sqlalchemy import create_engine

class QueryInterface():

    def daily_basic(self, ts_code, trade_date, start_date, end_date, custom_sql):
        engine = create_engine('mysql+pymysql://root:123456@localhost:3306/daily data')
        # db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="daily data", charset="utf8")
        # cursor = db.cursor()
        ts_filter = " AND ts_code = \'"+ts_code+"\'" if ts_code else "";
        trade_date_filter = ' AND trade_date = \''+trade_date+"\'" if trade_date else "";
        start_date_filter = ' AND trade_date > \''+start_date+"\'" if start_date else "";
        end_date_filter = ' AND trade_date < \''+end_date+"\'" if end_date else "";
        custom_sql_filter = custom_sql if custom_sql else "";
        sql = "SELECT * FROM DAILY WHERE 1=1 " + ts_filter + trade_date_filter + start_date_filter + end_date_filter + custom_sql_filter

        # cursor.execute(sql)
        # result = cursor.fetchall();
        # db.commit()
        result = pd.read_sql_query(sql, engine)
        return result

    def index_dayilybasic(self, ts_code, trade_date, start_date, end_date, custom_sql):
        engine = create_engine('mysql+pymysql://root:123456@localhost:3306/daily data')
        # db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="daily data", charset="utf8")
        # cursor = db.cursor()
        ts_filter = " AND ts_code = \'"+ts_code+"\'" if ts_code else "";
        trade_date_filter = ' AND trade_date = \''+trade_date+"\'" if trade_date else "";
        start_date_filter = ' AND trade_date > \''+start_date+"\'" if start_date else "";
        end_date_filter = ' AND trade_date < \''+end_date+"\'" if end_date else "";
        custom_sql_filter = custom_sql if custom_sql else "";
        sql = "SELECT * FROM INDEX_DAILYBASIC WHERE 1=1 " + ts_filter + trade_date_filter + start_date_filter + end_date_filter + custom_sql_filter

        # cursor.execute(sql)
        # result = cursor.fetchall();
        # db.commit()


        return result

if __name__ == '__main__':
    queryInterface = QueryInterface()
    queryInterface.index_dayilybasic('000001.SH', None, None, None, None)