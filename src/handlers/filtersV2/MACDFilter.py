# -*-coding=utf-8-*-
__author__ = 'aqua'

import numpy as np
import sys
sys.path.append('..')
from utils.Utils import Utils


class MACDFilter(object):
      pass

      def filter(self, data, config):
          return self.isMACDkingCross(data['df_3m'])

      def isMACDkingCross(self, df_3m):
          yesterday = df_3m.iloc[-2].get('macd')
          lastday = df_3m.iloc[-3].get('macd')
          now = df_3m.iloc[-1].get('macd')
          if np.isnan(yesterday) or np.isnan(now) or np.isnan(lastday):
             return False 
          return (yesterday < 0 and lastday < 0 and yesterday > lastday) and (now > 0 or round(float(now), 2) == 0.00)     
