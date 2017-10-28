# -*-coding=utf-8-*-
__author__ = 'aqua'

import numpy as np
import pandas as pd
import talib as ta

class Utils(object):
      pass
      
      @staticmethod
      def trendline(data, order=1):
         coeffs = np.polyfit(data.index.values, list(data), order)
         slope = coeffs[-2]
         return float(slope)

      @staticmethod
      def macd(df):
          close = df.close.values  #ndarray
          df['dif'], df['dea'], df['macd'] = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9) #series
          df['macd'] = df['macd'] * 2;