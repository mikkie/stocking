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