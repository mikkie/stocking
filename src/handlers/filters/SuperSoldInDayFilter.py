# -*-coding=utf-8-*-
__author__ = 'aqua'

from .StockFilter import StockFilter

class SuperSoldInDayFilter(StockFilter):
      pass

      def filter(self, data, config):
        #   print('今日当前5分钟K线 = ', data)
          high, low = self.getHighAnLowFromToday5MinK(data)
          if self.isInSuperSold(data, high, low, config): 
             return True
          return False

      def getHighAnLowFromToday5MinK(self, km5):
          return km5.loc[km5['close'].idxmax(), 'close'], km5.loc[km5['close'].idxmin(), 'close'] 


      #处于当天超售
      def isInSuperSold(self, km5, high, low, config):
          currentClose = km5.iloc[-1].get('close')
          currentPos = (currentClose - low) / (high - low)
        #   print('价格在当天位置=', currentPos)
          return currentPos < config.get_SuperSold()[1] and currentPos > config.get_SuperSold()[0]
      

      