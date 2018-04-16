# -*-coding=utf-8-*-
__author__ = 'aqua'

from ..MyLog import MyLog
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import datetime as dt
import math
import sys
sys.path.append('../..')
from config.Config import Config 
from utils.Utils import Utils
from t1.trade.trade import Trade
from t1.trade.MockTrade import MockTrade
import threading

class HitBottomAnalyze(object):
    
      def __init__(self):
          self.__config = Config()
          self.__buyedCount = 0
          self.__balance = self.__config.get_t1()['trade']['balance']
          if self.__config.get_t1()['trade']['enable']:
             self.__trade = Trade()
          if self.__config.get_t1()['trade']['enableMock']:
             self.__mockTrade = MockTrade()    
          self.__engine = create_engine(self.__config.get_DBurl())



      def printPerformace(self,timestamp):
          deltaSeconds = (dt.datetime.now() - timestamp).seconds 
          if deltaSeconds > 3: 
             print('calc more than %s seconds' % deltaSeconds)    

      def calcMain(self,dh,timestamp):
          data = dh.get_data()
          finalCode = ''
          result = []
          codes = []
          for code in data:
              if code in dh.get_buyed() or code in dh.get_ignore():
                 continue 
              try:  
                 if self.calc(data[code],dh):
                    result.append(data[code])
                #  self.printPerformace(timestamp)  
              except Exception as e:
                     last_line = data[code].get_Lastline()
                     MyLog.error(last_line['time'] + ' :calc ' + code + ' error')
                     MyLog.error(str(e))      
          if len(result) != 0:
             for stock in result: 
                 try:
                     last_line = stock.get_Lastline()
                     res = self.outputRes(last_line,timestamp)
                     if res is not None:
                        codes.append(stock.get_code())
                 except Exception as e:
                        MyLog.error('outputRes error %s' % stock.get_code())
                        MyLog.error(str(e))   
          return codes   


      def outputRes(self,df_final,timestamp):
          trade = self.__config.get_t1()['trade']
          if self.__buyedCount >= trade['max_buyed']:
             return None
          buyMoney = (float(df_final['price']) + trade['addPrice']) * trade['volume']  
          if buyMoney > self.__balance:
             return None   
          price = str('%.2f' % (float(df_final['price']) + trade['addPrice']))
          info = '[%s] 在 %s 以 %s 买入 [%s]%s %s 股' % (Utils.getCurrentTime(),str(df_final['date']) + ' ' + str(df_final['time']), price, df_final['code'], df_final['name'], str(trade['volume']))
          MyLog.info(info)
          now = dt.datetime.now()
          deltaSeconds = (now - timestamp).seconds
          if deltaSeconds > trade['timestampLimit']:
             MyLog.info('[%s] 行情超时 %s秒 放弃买入' % (df_final['code'],deltaSeconds)) 
             return None
          if trade['enable']:
             res = str(self.__trade.buy(df_final['code'],trade['volume'],float(price)))
             if 'entrust_no' in res:
                self.__buyedCount = self.__buyedCount + 1
                self.__balance = self.__balance - buyMoney
                return df_final['code']
             return None  
          if trade['enableMock']:
             res = self.__mockTrade.mockTrade(df_final['code'],float(price),trade['volume'])
             if res == 0:
                self.__buyedCount = self.__buyedCount + 1
                self.__balance = self.__balance - buyMoney
                return df_final['code']
             return None  
          return df_final['code']  


              
      def calc(self,stock,dh):
          ccp = self.getCurrentPercent(stock)
          if ccp >= self.__config.get_t1()['hitBottom']['max_p'] or ccp <= self.__config.get_t1()['hitBottom']['min_p']:
             return False
          lastLine = stock.get_Lastline()
          price = float(lastLine['price'])
          openPrice = float(lastLine['open'])
          high = float(lastLine['high'])
          low = float(lastLine['low'])
          if price >= openPrice or price <= low:
             return False
          return price - low <= (high - low) * self.__config.get_t1()['hitBottom']['margin']
                      

      def convertToFloat(self,str):
          if str == '':
             return 0 
          try:
              return float(str)
          except Exception as e:
                 MyLog.error('convertToFloat error: ' + str + '\n') 
                 return 0   


      def getPercent(self,price,stock):
          lastLine = stock.get_Lastline()
          pre_close = lastLine['pre_close']
          open_p = (float(price) - float(pre_close)) / float(pre_close) * 100
          return open_p
      
      def getCurrentPercent(self,stock):
          lastLine = stock.get_Lastline()
          price = lastLine['price']
          return self.getPercent(price,stock)
              

      def getOpenPercent(self,stock):
          ocp = stock.get_cache('ocp')
          if ocp is not None:
             return ocp 
          lastLine = stock.get_Lastline()
          open = lastLine['open']
          ocp = self.getPercent(open,stock)
          stock.set_cache('ocp',ocp)
          return ocp  

