import pandas_datareader.data as web
import  datetime

start = datetime.datetime(2016, 1, 1) # or start = '1/1/2016'
end = datetime.date.today()
jpy = web.DataReader('BTCUSD', 'stooq', start, end)
jpy.to_csv('usdjpy')
