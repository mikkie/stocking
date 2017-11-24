# -*-coding=utf-8-*-
__author__ = 'aqua'

import numpy as np
import sys
sys.path.append('..')
from utils.Utils import Utils

class LeftTradeFilter(object):
      pass

      def filter(self, data, config):
          df_3m = data['df_3m']
          df_3m = df_3m[config.get_trendPeriod() * -1:]
          high_row = df_3m.loc[df_3m['high'].idxmax()]
          high = high_row.get('high')
          low_row = df_3m.loc[df_3m['low'].idxmin()]
          low = low_row.get('low')
          close = df_3m.iloc[-1].get('close')
          if np.isnan(high) or np.isnan(low) or np.isnan(close):
             return False 
          ratio = (close - low) / (high - low) 
          high_date = high_row.get('date')
          low_date = low_row.get('date')
          return ratio < config.get_LeftTrade()[1] and ratio > config.get_LeftTrade()[0] and high_date < low_date