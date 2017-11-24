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
          df_3m = df_3m[config.get_LeftTrade()[0] * -1:]
          count = 0
          countH = 0
          lastClose = 0
          for index,row in df_3m.iterrows():
              if row['close'] > row['open']:
                 count = count + 1
              if lastClose != 0 and row['close'] > lastClose:
                 countH = countH + 1
              lastClose = row['close']      
          return count >= config.get_LeftTrade()[1] and countH >= config.get_LeftTrade()[2] and df_3m.iloc[-1]['close'] > df_3m.iloc[-1]['open']
                          