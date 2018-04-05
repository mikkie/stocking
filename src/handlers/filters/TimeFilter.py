# -*-coding=utf-8-*-
__author__ = 'aqua'

from .StockFilter import StockFilter

class TimeFilter(StockFilter):
      pass

      def filter(self, data, config):
          now = data.index[-1]
          return now >= config.get_StartTime()