# -*-coding=utf-8-*-
__author__ = 'aqua'

from .StockFilter import StockFilter

class IndicatorFilter(StockFilter):
      pass 

      def filter(self, data, config):
          return self.isMACDkingCross(data)

      def isMACDkingCross(self, km5):
          macd1 = km5.iloc[-2].get('macd')
          macd2 = km5.iloc[-1].get('macd')
          return (macd1 < 0 and macd2 >= 0) or (macd1 == 0 and macd2 > 0) 