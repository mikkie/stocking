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


      def getPercent(self,price,stock):
          lastLine = stock.get_Lastline()
          pre_close = lastLine.get('pre_close') 
          open_p = (float(price) - float(pre_close)) / float(pre_close) * 100
          return open_p
      
      def getCurrentPercent(self,stock):
          lastLine = stock.get_Lastline()
          price = lastLine.get('price')
          return self.getPercent(price,stock)
              

      def getOpenPercent(self,stock):
          lastLine = stock.get_Lastline()
          open = lastLine.get('open')
          return self.getPercent(open,stock)                


      def initLS(self,stock,dh):
          ccp = self.getCurrentPercent(stock)
          ls = ccp - self.__config.get_t1()['seller']['margin']
          if ls > self.__config.get_t1()['seller']['min_threshold']:
             stock.set_ls(ls)

      def calc(self,stock,dh):
          if stock.get_ls() is None:
             self.initLS()
          if stock.get_ls() is None:
             return False
          if self.getCurrentPercent(stock) < stock.get_ls():
             if self.sell(stock):
                dh.add_selled(stock.get_code()) 
          else:
               ccp = self.getCurrentPercent(stock)
               tls = ccp - self.__config.get_t1()['seller']['margin']
               if tls > stock.get_ls():
                  stock.set_ls(tls)   



      def sell(self,stock):
          last_line = stock.get_Lastline()
          price = float(str('%.2f' % (float(last_line['price']) - self.__config.get_t1()['trade']['minusPrice'])))
          return self.__mockTrade.sell(stock.get_code(),price)                    
