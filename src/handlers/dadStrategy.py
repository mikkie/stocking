# -*-coding=utf-8-*-
__author__ = 'aqua'

from .filters.SuperSoldInDayFilter import SuperSoldInDayFilter
from .filters.TimeFilter import TimeFilter
from .filters.RedCrossFilter import RedCrossFilter 
from .filters.VolumeFilter import VolumeFilter
from .filters.IndicatorFilter import IndicatorFilter
from datetime import datetime

class DadStrategy(object):
    

    def __init__(self):
        self.__filters = {'time' : TimeFilter(), 'superSold' : SuperSoldInDayFilter(), 'redCross' : RedCrossFilter(), 'volume' : VolumeFilter(), 'indicator' : IndicatorFilter()}

    def chooseStock(self, data, config):
        #时间到达14:25
        if self.__filters['time'].filter(data,config):
        #    print('===============监控开始,当前时间为:',datetime.now(),'==============')
           #处于当日超卖区20%内
           if self.__filters['superSold'].filter(data,config):
              #买盘量放大，卖盘量减小 
              if self.__filters['volume'].filter(data,config): 
                #金叉 
                if self.__filters['indicator'].filter(data,config): 
                   #出现十字星反转信号 
                   if self.__filters['redCross'].filter(data,config):  
                      return True 
        return False
