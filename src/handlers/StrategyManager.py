# -*-coding=utf-8-*-
__author__ = 'aqua'

from .filtersV2 import LeftTradeFilter, RightTradeFilter, MACDFilter, KDJFilter, TurnoverFilter, VolumeFilter, MAFilter, LongFlatFilter, MainForceTrendFilter

class StrategyManager(object):

      def __init__(self):
          self.strategyMaps = {}
          self.strategyMaps['leftTrade'] = LeftTradeFilter.LeftTradeFilter()
          self.strategyMaps['rightTrade'] = RightTradeFilter.RightTradeFilter()
          self.strategyMaps['macd'] = MACDFilter.MACDFilter()
          self.strategyMaps['kdj'] = KDJFilter.KDJFilter()
          self.strategyMaps['turnover'] = TurnoverFilter.TurnoverFilter()
          self.strategyMaps['volume'] = VolumeFilter.VolumeFilter()
          self.strategyMaps['ma'] = MAFilter.MAFilter()
          self.strategyMaps['flat'] = LongFlatFilter.LongFlatFilter()
          self.strategyMaps['bigMoney'] = MainForceTrendFilter.MainForceTrendFilter()


      def start(self,code,strategySequence,data,config):
          for ch in strategySequence:   
              if self.strategyMaps[ch].filter(data,config) == False:
                 data[ch] = 0 
                 return False  
              else:
                #  print('%s match strategy %s' % (code,ch)) 
                 data[ch] = 1    
                 pass  
          return True       

