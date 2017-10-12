# -*-coding=utf-8-*-
__author__ = 'aqua'

# import pandas as pd
# import numpy as np
import talib as ta
import tushare as ts
# from matplotlib import rc
# rc('mathtext', default='regular')
# import seaborn as sns
# sns.set_style('white')


dw = ts.get_k_data("300033")
close = dw.close.values
dw['dif'], dw['dea'], dw['macd'] = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
dw['macd'] = dw['macd'] * 2;
print(dw[['close','dif','dea','macd']])
# dw[['close','macd','macdsignal','macdhist']].plot()