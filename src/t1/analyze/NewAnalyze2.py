# -*-coding=utf-8-*-
__author__ = 'aqua'

from ..MyLog import MyLog
from sqlalchemy import create_engine
import tushare as ts
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

class NewAnalyze2(object):
    
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
              if code in dh.get_ignore():
                 continue
              if code in dh.get_buyed():
                 self.cancelBuyIfNeed(data[code],dh)
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


      def cancelBuyIfNeed(self,stock,dh):
          trade = self.__config.get_t1()['trade']
          now_line = stock.get_Lastline()
          now_buy1_v = self.convertToFloat(now_line['b1_v'])
          stop_price = round(float(now_line['pre_close']) * 1.1, 2)
          if float(now_line['price']) == stop_price:
             if float(now_line['b1_p']) == stop_price and self.convertToFloat(now_line['a1_v']) == 0 and (now_buy1_v * float(now_line['b1_p']) * 100) < self.__config.get_t1()['hit10']['cancel_b1_amount']:
                info = '[%s] 撤单 [%s],b1_v=%s' % (Utils.getCurrentTime(),stock.get_code(),now_buy1_v)
                if trade['enable']:
                   self.__trade.cancelBuy(stock.get_code()) 
                   MyLog.info(info)
                   dh.get_buyed().remove(stock.get_code())
                if trade['enableMock']:
                   status = self.__mockTrade.cancelBuy(stock.get_code())
                   if status == 0:
                      MyLog.info(info)
                      dh.get_buyed().remove(stock.get_code())  



      def outputRes(self,df_final,timestamp):
          trade = self.__config.get_t1()['trade']
          buyMoney = (float(df_final['price'])) * trade['volume']  
          if buyMoney > self.__balance:
             return None   
          price = str('%.2f' % (float(df_final['price'])))
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
                self.__balance = self.__balance - buyMoney
                return df_final['code']
             return None  
          if trade['enableMock']:
             res = self.__mockTrade.mockTrade(df_final['code'],float(price),trade['volume'])
             if res == 0:
                self.__balance = self.__balance - buyMoney
                return df_final['code']
             return None  
          return df_final['code']  


              
      def calc(self,stock,dh):
          if not self.canCalc(stock,dh):
             return False
          return self.isStockMatch(stock,dh)   

      def isOpenMatch(self,row):
          if float(row['pre_close']) == 0 or float(row['open']) == 0:
             return False
          return (float(row['open']) - float(row['pre_close'])) / float(row['pre_close']) * 100 >= -1.5


      def canCalc(self,stock,dh):
          if stock.len() < 0:
             return False
          lastLine = stock.get_Lastline() 
          if float(lastLine['open']) == 0.0:
             return False
          return True     


      def convertToFloat(self,str):
          if str == '':
             return 0 
          try:
              return float(str)
          except Exception as e:
                 MyLog.error('convertToFloat error: ' + str + '\n') 
                 return 0   


      def isStockMatch(self,stock,dh):
          if self.isZSMatch(stock):
             return self.isReach10(stock)


      def isReach10(self,stock):
          now_line = stock.get_Lastline()
          stop_price = round(float(now_line['pre_close']) * 1.1, 2)
          if float(now_line['price']) == stop_price:
             tag = float(now_line['b1_p']) == stop_price and self.convertToFloat(now_line['a1_v']) == 0 and (self.convertToFloat(now_line['b1_v']) * float(now_line['b1_p']) * 100) >= self.__config.get_t1()['hit10']['buy_b1_amount']  
             info = '[%s][%s] match 10,b1_v=%s' % (Utils.getCurrentTime(),stock.get_code(),now_line['b1_v'])
             MyLog.info(info)
             return tag 


      def isZSMatch(self,stock):
          zs = ts.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'])
          code = stock.get_code()
          i = 0
          if code.startswith('3'):
             i = 5 
          line = zs.iloc[i] 
          pre_close = line.get('pre_close') 
          price = line.get('price')
          p = (float(price) - float(pre_close)) / float(pre_close) * 100 
          return p > -0.3


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


              


              