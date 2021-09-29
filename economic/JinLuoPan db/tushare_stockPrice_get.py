# encoding=utf-8
#本文利用tushare开源数据库，存储并更新A股所有股票信息的前复权、后复权、不复权
#没有数据表，新建并插入有所有数据；有数据表，更新新数据
# 参数说明：http://tushare.waditu.com/

import economic as ts
import MySQLdb
import datetime

start_date='1990-01-01'
end_date='2017-06-01'#读取并更新此日期前上市的公司
min_insert_num = 5 #最少插入数据数目
today_date=datetime.date.today().strftime('%Y-%m-%d')#读取并更新此日期前的交易数据

db1 = MySQLdb.connect(host="localhost", user="root", passwd="123", db="golden compass", charset="utf8")
db2 = MySQLdb.connect(host="localhost", user="root", passwd="123", db="price data", charset="utf8")
cursor1 = db1.cursor()

############################################################################更新公司信息数据库
stock_set = ts.get_stock_basics()#从tushare获得所有的公司信息，并更新数据库
size = len(stock_set);
for i in range(size):
    cursor1.execute(
        "insert ignore into stockInfo(code,name,industry,area,pe,outstanding,totals,totalAssets,liquidAssets,fixedAssets,reserved,reservedPerShare,esp,bvps,pb,timeToMarket,undp,perundp,rev,profit,gpr,npr,holders)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (stock_set.axes[0][i],stock_set.name[i],stock_set.industry[i],stock_set.area[i],stock_set.pe[i],stock_set.outstanding[i],stock_set.totals[i],stock_set.totalAssets[i],stock_set.liquidAssets[i],stock_set.fixedAssets[i],stock_set.reserved[i],stock_set.reservedPerShare[i],stock_set.esp[i],stock_set.bvps[i],stock_set.pb[i],str(stock_set.timeToMarket[i]),stock_set.undp[i],stock_set.perundp[i],stock_set.rev[i],stock_set.profit[i],stock_set.gpr[i],stock_set.npr[i],stock_set.holders[i]))
db1.commit();

############################################################################更新价格数据库
cursor1.execute("select code from stockInfo where timeToMarket >%s and timeToMarket <%s",(start_date,end_date))
result=cursor1.fetchall()#得到start_date和end_date之间上市的所有股票代码
cursor1.close()

for i in range(len(result)):#遍历更新数据
    stock_code="".join(result[i]).encode("utf-8")
    table_name = "a" +stock_code
    print(table_name)

    cursor2 = db2.cursor()
    if cursor2.execute("SHOW TABLES LIKE %s",table_name)==0:#不存在此表，新建数据表
        sql2="CREATE TABLE "+table_name+"(date date PRIMARY KEY, open VARCHAR(10), close VARCHAR(10), high VARCHAR(10), low VARCHAR(10), volume VARCHAR(10), open_before VARCHAR(10), close_before VARCHAR(10), high_before VARCHAR(10), low_before VARCHAR(10), volume_before VARCHAR(10), open_after VARCHAR(10), close_after VARCHAR(10), high_after VARCHAR(10), low_after VARCHAR(10), volume_after VARCHAR(10))"
        cursor2.execute(sql2)#新建数据表
        db2.commit()

        data_None = ts.get_k_data(stock_code, ktype='D',autype='None', start=start_date, end=today_date)  # 获取全部不复权日数据
        data_before = ts.get_k_data(stock_code, ktype='D',autype='qfq', start=start_date, end=today_date)  # 获取全部不复权日数据
        data_after = ts.get_k_data(stock_code, ktype='D',autype='hfq', start=start_date, end=today_date)  # 获取全部不复权日数据

        data_size = len(data_None.date);
        if data_size < min_insert_num:#数据太少，放弃插入
            print("新建数据表，更新数据太少，放弃添加数据",data_size)
            continue
        else:
            for i in range(data_size):
                cursor2.execute("insert ignore into " + table_name + "(date,open,close,high,low,volume,open_before,close_before,high_before,low_before,volume_before,open_after,close_after,high_after,low_after,volume_after) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(data_None.date[i],data_None.open[i],data_None.close[i],data_None.high[i],data_None.low[i],data_None.volume[i],data_before.open[i],data_before.close[i],data_before.high[i],data_before.low[i],data_before.volume[i],data_after.open[i],data_after.close[i],data_after.high[i],data_after.low[i],data_after.volume[i]))  # 插入数据
            db2.commit()
            print ("新建数据表，添加数据数据成功")

    else:#若存在此表，则更新数据
        sql = "select max(date) from "+table_name
        cursor2.execute(sql)
        temp = cursor2.fetchall()#获得已存在表的最新日期
        latest_date = str(temp[0][0])
        if latest_date != 'None':#原表有数据
            data_None_update = ts.get_k_data(stock_code, ktype='D', autype='None', start=latest_date, end=today_date)  # 获取全部不复权日数据
            data_before_update = ts.get_k_data(stock_code, ktype='D', autype='qfq', start=latest_date, end=today_date)  # 获取全部不复权日数据
            data_after_update = ts.get_k_data(stock_code, ktype='D', autype='hfq', start=latest_date, end=today_date)  # 获取全部不复权日数据

            data_update_size = len(data_None_update.date);
            if data_update_size < min_insert_num:#数据太少，放弃插入
                print("已存在数据表，更新数据太少，放弃添加数据")
                continue
            else:
                init_index = data_None_update.first_valid_index()#获得开始索引
                for i in range(init_index+1,init_index+data_update_size):
                    cursor2.execute(
                        "insert ignore into " + table_name + "(date,open,close,high,low,volume,open_before,close_before,high_before,low_before,volume_before,open_after,close_after,high_after,low_after,volume_after) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (data_None_update.date[i], data_None_update.open[i], data_None_update.close[i], data_None_update.high[i], data_None_update.low[i],data_None_update.volume[i], data_before_update.open[i], data_before_update.close[i], data_before_update.high[i],data_before_update.low[i],data_before.volume[i],data_after_update.open[i], data_after_update.close[i], data_after_update.high[i],data_after_update.low[i],data_after.volume[i]))  # 插入数据
                db2.commit()
                print( "已存在数据表，添加数据数据成功")
        else:#原表里没有数据
            data_None = ts.get_k_data(stock_code, ktype='D', autype='None', start=start_date, end=today_date)  # 获取全部不复权日数据
            data_before = ts.get_k_data(stock_code, ktype='D', autype='qfq', start=start_date, end=today_date)  # 获取全部不复权日数据
            data_after = ts.get_k_data(stock_code, ktype='D', autype='hfq', start=start_date, end=today_date)  # 获取全部不复权日数据

            data_size = len(data_None.date);
            if data_size < min_insert_num: #数据太少，放弃插入
                print ("已存在数据表，更新数据太少，放弃添加数据", data_size)
                continue
            else:
                for i in range(data_size):
                    cursor2.execute(
                        "insert ignore into " + table_name + "(date,open,close,high,low,volume,open_before,close_before,high_before,low_before,volume_before,open_after,close_after,high_after,low_after,volume_after) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (data_None.date[i], data_None.open[i], data_None.close[i], data_None.high[i], data_None.low[i],
                         data_None.volume[i], data_before.open[i], data_before.close[i], data_before.high[i],
                         data_before.low[i], data_before.volume[i], data_after.open[i], data_after.close[i], data_after.high[i],
                         data_after.low[i],data_after.volume[i]))  # 插入数据
                db2.commit()
                print ("已存在数据表，没有数据，重新添加数据数据成功")
db1.close()
db2.close()
