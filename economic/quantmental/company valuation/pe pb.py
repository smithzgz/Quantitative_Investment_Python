import matplotlib.pyplot as plt

import generate_query_interface as query
import tushare_test as ts
import pandas as pd
from sqlalchemy import create_engine

from mpl_toolkits.mplot3d import Axes3D  #绘制三D图形
# pro = ts.pro_api()
#
# # 获取股票基本信息，包括 PE、PB 值
# df_base = pro.daily_basic(ts_code='', trade_date='20180810')
# #df_base['code'] = df_base.index
#
# # 获取股票当天数据，包括当前股价
#
# df_todays = pro.daily(trade_date='20180810')
# #df_todays['code'] = df_todays.index
#
# # 整合股价与 PE、PB 数据
# df = pd.merge(df_todays, df_base, how='right', on=['ts_code'])
queryInterface = query.QueryInterface()
df = queryInterface.daily_basic('000001.SZ', None, None, None, None)
#df = queryInterface.daily_basic(None, '20190510', None, None, None)

pe = df['pe'].tolist()  # X 轴为 PE 数据
pb = df['pb'].tolist()  # Y 轴为 PB 数据
price = df['high'].tolist()  # Z 轴为 股价数据
time = df["trade_date"].tolist() # 时间

plt.subplot(221)
plt.plot(time, pe,"ro")
plt.subplot(212)
plt.plot(time, pb,"ro")
plt.subplot(222)
plt.plot(time, price,"ro")

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# #给三个坐标轴注明
# ax.set_xlabel('PE', color='r')
# ax.set_ylabel('PB', color='g')
# ax.set_zlabel('trade', color='b')
# ax.scatter(X, Y, Z)


plt.show()