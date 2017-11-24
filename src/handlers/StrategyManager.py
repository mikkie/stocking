# -*-coding=utf-8-*-
__author__ = 'aqua'

from .filtersV2 import LeftTradeFilter, RightTradeFilter, MACDFilter, KDJFilter

class StrategyManager(object):

      def __init__(self):
          self.strategyMaps = {}
          self.strategyMaps['leftTrade'] = LeftTradeFilter.LeftTradeFilter()
          self.strategyMaps['rightTrade'] = RightTradeFilter.RightTradeFilter()
          self.strategyMaps['macd'] = MACDFilter.MACDFilter()
          self.strategyMaps['kdj'] = KDJFilter.KDJFilter()


      def start(self,code,strategySequence,data,config):
          for ch in strategySequence:   
              if self.strategyMaps[ch].filter(data,config) == False:
                 return False  
              else:
                #  print('%s match strategy %s' % (code,ch))    
                 pass  
          return True       

