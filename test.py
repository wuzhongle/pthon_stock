# 来自文章
# https://blog.51cto.com/youerning/2428352?source=dra

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import talib
import tushare as ts
# pip install https://github.com/matplotlib/mpl_finance/archive/master.zip
from mpl_finance import candlestick_ohlc
from matplotlib.pylab import date2num
import global_value
import math
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
'''
上面两句话我也不知道为啥要加，不加会报Warning---
FutureWarning: Using an implicitly registered datetime converter for a matplotlib plotting method. 
The converter was registered by pandas on import. 
Future versions of pandas will require you to explicitly register matplotlib converters.
'''

daily_data_position = global_value.local_position + 'fig/'

# 使用ggplot样式，好看些
mpl.style.use("ggplot")
# 获取上证指数数据
stock_code = "000001"
start_time = "2019-01-01"
data = ts.get_k_data(stock_code, index=True, start=start_time)
# 将date值转换为datetime类型，并且设置成index
data.date = pd.to_datetime(data.date)
data.index = data.date

# 计算移动平均线
data["ma10"] = talib.MA(data.close, timeperiod=10)
data["ma30"] = talib.MA(data.close, timeperiod=30)

# 计算RSI
data["rsi"] = talib.RSI(data.close)

# 计算MACD指标数据
data["macd"], data["signal"], data["hist"] = talib.MACD(data.close)

# EMA
data["ema22"] = talib.MA(data.close, timeperiod=22)
data["ema11"] = talib.MA(data.close, timeperiod=11)

# 计算RSI
data["rsi"] = talib.RSI(data.close)

# 绘制第一个图
fig = plt.figure()
fig.set_size_inches((16, 20))

ax_canddle = fig.add_axes((0, 0.7, 1, 0.3))
ax_macd = fig.add_axes((0, 0.45, 1, 0.2))
ax_rsi = fig.add_axes((0, 0.23, 1, 0.2))
ax_vol = fig.add_axes((0, 0, 1, 0.2))

data_list = []
for date, row in data[["open", "high", "low", "close"]].iterrows():
    t = date2num(date)
    open, high, low, close = row[:]
    datas = (t, open, high, low, close)
    data_list.append(datas)

# 绘制蜡烛图
candlestick_ohlc(ax_canddle, data_list, colorup='r', colordown='green', alpha=0.7, width=0.8)
# 将x轴设置为时间类型
ax_canddle.xaxis_date()
ax_canddle.plot(data.index, data.ma10, label="MA10")
ax_canddle.plot(data.index, data.ma30, label="MA30")
ax_canddle.plot(data.index, data.ema22, label="EMA11")
ax_canddle.plot(data.index, data.ema11, label="EMA22")
ax_canddle.legend()

# 绘制MACD
ax_macd.plot(data.index, data["macd"], label="macd")
ax_macd.plot(data.index, data["signal"], label="signal")
ax_macd.bar(data.index, data["hist"] * 2, label="hist")
ax_macd.legend()

# 绘制RSI
# 超过85%设置为超买, 超过20%为超卖
ax_rsi.plot(data.index, [80] * len(data.index), label="overbuy")
ax_rsi.plot(data.index, [20] * len(data.index), label="oversell")
ax_rsi.plot(data.index, data.rsi, label="rsi")
ax_rsi.set_ylabel("%")
ax_rsi.legend()

# 将volume除以100w
ax_vol.bar(data.index, data.volume / 1000000)
# 设置成百万位单位
ax_vol.set_ylabel("millon")
ax_vol.set_xlabel("date")
fig.savefig(daily_data_position + "index.png")

# 标记移动平均线买入卖出点
# for date, point in data[["ma_point"]].itertuples():
#     if math.isnan(point):
#         continue
#     if point > 0:
#         ax_canddle.annotate("",
#                             xy=(date, data.loc[date].close),
#                             xytext=(date, data.loc[date].close - 10),
#                             arrowprops=dict(facecolor="r",
#                                             alpha=0.3,
#                                             headlength=10,
#                                             width=10))
#     elif point < 0:
#         ax_canddle.annotate("",
#                             xy=(date, data.loc[date].close),
#                             xytext=(date, data.loc[date].close + 10),
#                             arrowprops=dict(facecolor="g",
#                                             alpha=0.3,
#                                             headlength=10,
#                                             width=10))
