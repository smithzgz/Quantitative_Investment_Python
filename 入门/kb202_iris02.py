import pandas as pd  # 该工具是为解决数据分析任务而创建的
import tushare as ts
import matplotlib as mpl
import plotly
import arrow

# 爱丽丝进化和文本矢量化
# 鸢尾花数据集,前四列萼片长度, 萼片宽度,花瓣长度, 花瓣宽度.最后一列0，1,2分别是setosa, versicolor, virginica
fss = 'data/iris.csv'
df = pd.read_csv(fss, index_col=False)

xlst, ysgn = ['x1', 'x2', 'x3', 'x4'], 'xid'
x, y = df[xlst], df[ysgn]
print('\n #2 xlist', xlst)