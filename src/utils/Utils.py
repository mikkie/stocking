# -*-coding=utf-8-*-
__author__ = 'aqua'

import numpy as np
import pandas as pd
import talib as ta

class Utils(object):
      pass
      
      @staticmethod
      def trendline(data, order=1):
         values = list(data)
         coeffs = np.polyfit(list(range(1,len(values) + 1)), values, order)
         slope = coeffs[-2]
         return float(slope)

      @staticmethod
      def macd(df):
          close = df.close.values  #ndarray
          df['dif'], df['dea'], df['macd'] = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9) #series
          df['macd'] = df['macd'] * 2;

      @staticmethod
      def kdj(df): 
          close = df.close.values  #ndarray
          high = df.high.values
          low = df.low.values
          df['k'], df['d'] = ta.STOCH(high, low, close, fastk_period=9, slowk_period=3, slowk_matype=1, slowd_period=3, slowd_matype=1)
          df['j'] = 3 * df['k'] - 2 * df['d']

      @staticmethod
      def myKdj(df):
          low_list = df.low.rolling(center=False,window=9).min()
          low_list.fillna(value=df.low.expanding(min_periods=1).min(),inplace=True)   
          high_list = df.high.rolling(center=False,window=9).max()
          high_list.fillna(value=df.high.expanding(min_periods=1).max(),inplace=True)   
          rsv = (df.close - low_list) / (high_list - low_list) * 100
          df['k'] = rsv.ewm(com=2,adjust=True,ignore_na=False,min_periods=0).mean()
          df['d'] = df.k.ewm(com=2,adjust=True,ignore_na=False,min_periods=0).mean()
          df['j'] = 3 * df['k'] - 2 * df['d']