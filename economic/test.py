import tushare as ts
pro = ts.pro_api()
token= "47105aced0d886b2c9544eccf752c1b952eb109379a80def6119691f"
ts.set_token(token)
# 获取个股资金流向
df_moneyflow = pro.stk_holdernumber(ts_code='601318.SH', start_date='20000101', end_date='20211231')
print(df_moneyflow)


