# -*-coding=utf-8-*-
__author__ = 'aqua'

from .StockFilter import StockFilter

class TimeFilter(StockFilter):
      pass

      def filter(self, data, config):
          km5 = data['km5']
          now = km5.iloc[-1].get('date')
          return now >= config.get_StartTime()