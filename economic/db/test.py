import sys
import tushare as ts
import pandas as pd
import MySQLdb
import matplotlib.pyplot as plt
import generate_query_interface as query
from sqlalchemy import create_engine
import numpy as np

pro = ts.pro_api()
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/daily data')
db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="daily data", charset="utf8")
cursor = db.cursor()
result = pd.read_sql_query('select DISTINCT ts_code from daily ', engine)

a = np.arange(0,8,1)
print(a)

# 查询当前所有正常上市交易的股票列表
# ts_count = 0
# for ts_code in result.values:
#     ts_count = ts_count+1;
#     print("////////////////////////////////", ts_count)
#     # 获得复权因子
#     df_adj_factor = pro.adj_factor(ts_code=ts_code[0])
#     # 获取个股资金流向
#     df_moneyflow = pro.moneyflow(ts_code=ts_code[0])
#     df_data = pd.merge(df_moneyflow, df_adj_factor, how='right', on=['trade_date'])
#
#     index_data = ["buy_sm_vol","buy_sm_amount","sell_sm_vol","sell_sm_amount","buy_md_vol","buy_md_amount","sell_md_vol","sell_md_amount","buy_lg_vol","buy_lg_amount","sell_lg_vol","sell_lg_amount","buy_elg_vol","buy_elg_amount","sell_elg_vol","sell_elg_amount","net_mf_vol","net_mf_amount","adj_factor"]
#
#     count = 0
#     for trade_date in df_data['trade_date']:
#         sql = "select count(*) from daily " + " where ts_code = '"+ts_code+"' and trade_date ='"+trade_date+"'"
#         result = pd.read_sql_query(sql[0], engine)
#
#         if(result.values[0][0]==1):
#             sql_before = "update daily set "
#             sql_after = " where ts_code = '"+ts_code+"' and trade_date ='"+trade_date+"'"
#             sql_middle = ""
#
#             for index in index_data:
#                 if (pd.isnull(df_data[index][count])):
#                     continue
#                 else:
#                     sql_middle += index + " = '" + str(df_data[index][count]).replace("'", "\\\'") + "',"
#
#             sql = sql_before+sql_middle.strip(",\n") +sql_after
#             # print(sql[0])
#             # pd.read_sql_query(sql[0], engine)
#             cursor.execute(sql[0])
#             db.commit()
#         count = count + 1
# sys.exit(0)
