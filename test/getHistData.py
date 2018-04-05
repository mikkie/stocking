# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import talib as ta
import pandas as pd
from sqlalchemy import create_engine

code = '600153'

def myMACD(price, fastperiod=12, slowperiod=26, signalperiod=9):
    ewma12 = pd.ewma(price,span=fastperiod)
    ewma60 = pd.ewma(price,span=slowperiod)
    dif = ewma12-ewma60
    dea = pd.ewma(dif,span=signalperiod)
    bar = 2 * (dif-dea) #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
    return dif,dea,bar

df_hist = ts.get_hist_data(code,start='2017-10-24',ktype='5')
df_hist = df_hist.iloc[::-1]
close = df_hist.close.values
df_hist['dif'], df_hist['dea'], df_hist['macd'] = myMACD(close, fastperiod=12, slowperiod=26, signalperiod=9) #series

print(df_hist)
engine = create_engine('mysql://root:aqua@192.168.1.4/stocking?charset=utf8')
df_hist.to_sql('km5',engine,if_exists='append')