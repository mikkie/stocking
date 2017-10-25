# -*-coding=utf-8-*-
__author__ = 'aqua'

from .StockFilter import StockFilter

class SuperSoldInDayFilter(StockFilter):
      pass

      def filter(self, data, config):
          print('前三天日K线 = ', data['kd3'])
          print('今日当前5分钟K线 = ', data['km5'])
          high, low = self.getHighAnLowFromToday5MinK(data['km5'])
          if self.isChangeMatch(data['kd3'], high, low, config):
             if self.isInSuperSold(data['km5'], high, low, config): 
                return True
          return False

      def getHighAnLowFromToday5MinK(self, km5):
          return km5.loc[km5['close'].idxmax(), 'close'], km5.loc[km5['close'].idxmin(), 'close'] 


      #处于当天超售
      def isInSuperSold(self, km5, high, low, config):
          currentClose = km5.iloc[-1].get('close')
          currentPos = (currentClose - low) / (high - low)
          print('价格在当天位置=', currentPos)
          return currentPos < config.get_SuperSold()[1] and currentPos > config.get_SuperSold()[0]
      
      #振幅是否足够
      def isChangeMatch(self, kd3, high, low, config):
          lastDayClose = kd3.iloc[-1].get('close')
          change = (high - low) / lastDayClose
          print('振幅=' , change)
          return change > config.get_pKm5Change()