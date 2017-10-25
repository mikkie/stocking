# -*-coding=utf-8-*-
__author__ = 'aqua'

from .StockFilter import StockFilter
import sys
sys.path.append('..')
from utils.Utils import Utils

class VolumeFilter(StockFilter):
      pass

      def filter(self, data, config):
          km5 = data['km5']
          sellVolume = self.getSellVolume(km5)
          sellTrend = Utils.trendline(sellVolume['volume'])
          print('sellVolumn and trend', sellVolume['volume'], sellTrend)
          buyVolume = self.getBuyVolume(km5) 
          buyTrend = Utils.trendline(buyVolume['volume'])
          print('buyVolume and trend', buyVolume['volume'], buyTrend)
          return sellTrend < 0 and buyTrend > 0


      def getSellVolume(self, km5):
          return km5[km5['open'] > km5['close']]

      def getBuyVolume(self, km5):
          return km5[km5['open'] < km5['close']]       