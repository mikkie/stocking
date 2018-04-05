# -*-coding=utf-8-*-
__author__ = 'aqua'

from .StockFilter import StockFilter
import numpy as np

class RedCrossFilter(StockFilter):
      pass

      def filter(self, data, config):
          return self.isRedCross(data)
       
      def isRedCross(self,km5):
          open = km5.iloc[-1].get('open')
          close = km5.iloc[-1].get('close')
          low = km5.iloc[-1].get('low')
          md5 = km5.iloc[-1].get('ma5')
          if np.isnan(open) or np.isnan(close) or np.isnan(low) or np.isnan(md5):
             return False 
          if open == close and low >= md5:
             print('出现十字星,且当前最低价>md5,当前价格=' , close) 
             return True
          return False