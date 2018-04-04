# -*-coding=utf-8-*-
__author__ = 'aqua'

from ..MyLog import MyLog
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import datetime as dt
import cmath
import sys
sys.path.append('../..')
from config.Config import Config 
from utils.Utils import Utils
from t1.trade.trade import Trade
from t1.trade.MockTrade import MockTrade
import threading

class SellAnalyze(object):

      def __init__(self):
          self.__config = Config()
          if self.__config.get_t1()['trade']['enable']:
             self.__trade = Trade()
          if self.__config.get_t1()['trade']['enableMock']:
             self.__mockTrade = MockTrade()    
          self.__engine = create_engine(self.__config.get_DBurl())

      def calcMain(self,dh):
          data = dh.get_data()
          for code in data:
              if len(dh.get_selled()) > 0:
                 if code in dh.get_selled():
                    continue 
              try:  
                 if self.calc(data[code],dh):
                    dh.add_selled(code,True)
              except Exception as e:
                     last_line = data[code].get_Lastline()
                     MyLog.error(last_line['time'] + ' :calc ' + code + ' error')
                     MyLog.error(str(e))  


      def calc(self,stock,dh):
          pass                       