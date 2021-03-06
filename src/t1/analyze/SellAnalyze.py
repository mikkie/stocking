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
             self.__trade = Trade(isSell=True)
          if self.__config.get_t1()['trade']['enableMock']:
             self.__mockTrade = MockTrade()    
          self.__engine = create_engine(self.__config.get_DBurl())

      def calcMain(self,zs,dh):
          data = dh.get_data()
          for code in data:
              if len(dh.get_selled()) > 0:
                 if code in dh.get_selled():
                    continue 
              try:  
                 if self.calc(zs,data[code],dh):
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


      def initLS(self,stock,dh,ratio):
          ccp = self.getCurrentPercent(stock)
          ls = ccp - self.__config.get_t1()['seller']['margin'][stock.get_code()] * ratio
          if ls > self.__config.get_t1()['seller']['min_threshold']:
             stock.set_ls(ls)

      def calc(self,zs,stock,dh):
          ratio = 1
          stop_loss = self.__config.get_t1()['seller']['stop_loss_win']['loss_good']
          stop_win = self.__config.get_t1()['seller']['stop_loss_win']['win_good']
          if self.isZSMatch(zs,stock):
             ratio = self.__config.get_t1()['seller']['ratio']
             stop_loss = self.__config.get_t1()['seller']['stop_loss_win']['loss_bad']
             stop_win = self.__config.get_t1()['seller']['stop_loss_win']['win_bad']
          if self.getCurrentPercent(stock) < stop_loss:
             stock.add_sellSignal()
             if stock.get_sellSignal() > self.__config.get_t1()['seller']['maxSellSignal']: 
                return self.sell(stock)
             return False
          if self.getCurrentPercent(stock) >= stop_win:
             stock.set_cache('start_stop_win',True)
          if stock.get_cache('start_stop_win') is None:
             return False    
          if stock.get_ls() is None:
             self.initLS(stock,dh,ratio)
             if stock.get_ls() is None:
                return False
          if self.getCurrentPercent(stock) < stock.get_ls():
             stock.add_sellSignal()
             if stock.get_sellSignal() > self.__config.get_t1()['seller']['maxSellSignal']: 
                return self.sell(stock)
             return False
          else:
               stock.reset_sellSignal()
               ccp = self.getCurrentPercent(stock)
               tls = ccp - self.__config.get_t1()['seller']['margin'][stock.get_code()] * ratio
               if tls > stock.get_ls():
                  stock.set_ls(tls) 
               return False     


      def can_sell(self,stock):
          last_sell_time = stock.get_cache('last_sell_time')      
          if last_sell_time is None:
             stock.set_cache('last_sell_time',dt.datetime.now())
             return True 
          now = dt.datetime.now()
          if (now - last_sell_time).seconds > 30:
             stock.set_cache('last_sell_time',now)
             return True
          return False   
              
              

      def isZSMatch(self,zs,stock):
          if zs is None:
             return True 
          code = stock.get_code()
          i = 0
          if code.startswith('3'):
             i = 5 
          line = zs.iloc[i] 
          pre_close = line.get('pre_close') 
          price = line.get('price')
          p = (float(price) - float(pre_close)) / float(pre_close) * 100 
          return p < 0


      def sell(self,stock):
          if not self.can_sell(stock):
             return False 
          last_line = stock.get_Lastline()
          price = float(str('%.2f' % (float(last_line['price']) - self.__config.get_t1()['trade']['minusPrice'])))
          info = '[%s] 在 %s 以 %s 卖出 [%s]%s 全部股票' % (Utils.getCurrentTime(),str(last_line['date']) + ' ' + str(last_line['time']), price, last_line['code'], last_line['name'])
          MyLog.info(info)
          if self.__config.get_t1()['trade']['enable']:
             return self.__trade.sell(stock.get_code(),price)
          elif self.__config.get_t1()['trade']['enableMock']:
               return self.__mockTrade.sell(stock.get_code(),price) 
          return True   
