import pandas as pd  # 该工具是为解决数据分析任务而创建的
import tushare_test as ts
import matplotlib as mpl
import plotly
import arrow

# 鸢尾花数据集,前四列萼片长度, 萼片宽度,花瓣长度, 花瓣宽度.最后一列0，1,2分别是setosa, versicolor, virginica
fss = 'data/iris.csv'
df = pd.read_csv(fss, index_col=False)
print('\n #1 df')
# tail尾5行，head()头五行
# describe() #统计数据
# df.T #转置
print(df.head())
print(df.tail())
print(df.describe())

#2
#value_counts()是一种查看表格某列中有多少个不同值
d10=df['xname'].value_counts()
print('\n #2 xname')
print(d10)