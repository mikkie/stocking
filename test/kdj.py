# -*-coding=utf-8-*-
__author__ = 'aqua'

# import pandas as pd
# import numpy as np
import talib as ta
import tushare as ts


def kdj(df): 
    close = df.close.values  #ndarray
    high = df.high.values
    low = df.low.values
    df['k'], df['d'] = ta.STOCH(high, low, close, fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    df['j'] = 3 * df['k'] - 2 * df['d']

df_h = ts.get_hist_data('600848')
df_h = df_h[::-1]
kdj(df_h)
print(df_h)