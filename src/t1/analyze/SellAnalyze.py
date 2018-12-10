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


      def getWinLossPercent(self,stock):
          buy_price = stock.get_cache('buy_price')
          if buy_price is None:
             state = self.__config.get_t1()['seller']['state']   
             buy_price = state[stock.get_code()]['price']
             stock.set_cache('buy_price',buy_price)  
          return self.getPercent(buy_price,stock)    
              

      def getOpenPercent(self,stock):
          lastLine = stock.get_Lastline()
          open = lastLine.get('open')
          return self.getPercent(open,stock)                


      def initLS(self,stock,dh,ratio):
          ccp = self.getWinLossPercent(stock)
          ls = ccp - self.__config.get_t1()['seller']['margin'][stock.get_code()] * ratio
          if ls > self.__config.get_t1()['seller']['min_threshold']:
             stock.set_ls(ls)


      def convertToFloat(self,str):
          if str == '':
             return 0 
          try:
              return float(str)
          except Exception as e:
                 MyLog.error('convertToFloat error: ' + str + '\n') 
                 return 0


      def is_bc_point(self, stock, dh):
          now_line = stock.get_Lastline()
          now_price = self.convertToFloat(now_line['price'])
          lowest_price = self.convertToFloat(now_line['low'])
          if now_price == lowest_price or (now_price - lowest_price) / self.convertToFloat(now_line['pre_close']) * 100 > self.__config.get_t1()['bc_point']['p_limit_lowest']:
             return False
          datas = stock.get_data()
          start = -15
          if len(datas) < start * -1:
             start = len(datas) * -1 
          amount = self.convertToFloat(datas[-1]['buy_amount']) - self.convertToFloat(datas[start]['buy_amount'])
          sell_amount = self.convertToFloat(datas[-1]['sell_amount']) - self.convertToFloat(datas[start]['sell_amount'])
          amount_ratio = 100
          if sell_amount != 0.0:
             amount_ratio = amount / sell_amount 
          tag = amount > self.__config.get_t1()['bc_point']['min_amount'] and amount_ratio > self.__config.get_t1()['bc_point']['amount_ratio'] 
          if tag:
             MyLog.info('bc buy match: time = %s, lowest_price = %s, buy_amount = %s, sell_amount = %s, amount_ratio = %s' % (now_line['date'] + ' ' + now_line['time'], lowest_price, amount, sell_amount, amount_ratio)) 
          return tag


      def is_bc_sell(self, stock):
          now_line = stock.get_Lastline()
          buy_price = stock.get_cache('buy_price')
          if buy_price is None:
             return False 
          if (self.convertToFloat(now_line['price']) - buy_price) / self.convertToFloat(now_line['pre_close']) * 100 >= self.__config.get_t1()['seller']['bc_sell_profit']:
             return True 
          return False


      def is_ydxd(self, stock):
          datas = stock.get_data()
          now_price = self.convertToFloat(data[-1]['price'])
          start = -20
          if len(datas) < 20:
             start = len(data) * -1
          temp = data[start:-1]
          high = None
          low = None
          for row in temp:
              price = self.convertToFloat(row['price'])
              if high is None or price > high:
                 high = price
              if low is None or price < low:
                 low = price    
          if (high - now_price) / self.convertToFloat(data[-1]['pre_close']) * 100 < self.__config.get_t1()['seller']['ydxd']:
             return False
          if now_price == low or (now_price - low) / self.convertToFloat(data[-1]['pre_close']) * 100 > self.__config.get_t1()['bc_point']['p_limit_lowest']:
             return False
          return True   


                     



      def calc(self,zs,stock,dh):
          if stock.get_cache('buy_price') is not None:
             if self.is_bc_sell(stock):
                return self.sell(stock)
             return False
          ratio = 1
          stop_loss = self.__config.get_t1()['seller']['stop_loss_win']['loss_good']
          stop_win = self.__config.get_t1()['seller']['stop_loss_win']['win_good']
          if self.isZSMatch(zs,stock):
             ratio = self.__config.get_t1()['seller']['ratio']
             stop_loss = self.__config.get_t1()['seller']['stop_loss_win']['loss_bad']
             stop_win = self.__config.get_t1()['seller']['stop_loss_win']['win_bad']
          if self.getWinLossPercent(stock) < stop_loss and self.getCurrentPercent(stock) < stop_loss:
             now_line = stock.get_Lastline()
             if now_line['time'] > '14:30:00':
                return False
             if self.is_bc_point(stock) or self.is_ydxd(stock):
                return self.bc_buy(stock)  
            #  stock.add_sellSignal()
            #  if stock.get_sellSignal() > self.__config.get_t1()['seller']['maxSellSignal']: 
            #     return self.sell(stock)
             return False
          if self.getWinLossPercent(stock) >= stop_win:
             stock.set_cache('start_stop_win',True)
          if stock.get_cache('start_stop_win') is None:
             return False    
          if stock.get_ls() is None:
             self.initLS(stock,dh,ratio)
             if stock.get_ls() is None:
                return False
          if self.getWinLossPercent(stock) < stock.get_ls():
             stock.add_sellSignal()
             if stock.get_sellSignal() > self.__config.get_t1()['seller']['maxSellSignal']: 
                return self.sell(stock)
             return False
          else:
               stock.reset_sellSignal()
               ccp = self.getWinLossPercent(stock)
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


      def bc_buy(self, stock):
          df_final = stock.get_Lastline()     
          p = (float(df_final['price']) - float(df_final['pre_close'])) / float(df_final['pre_close'])
          d_price = round(float(df_final['pre_close']) * (1 + p + 0.005), 2)
          price = str('%.2f' % d_price)
          state = self.__config.get_t1()['seller']['state']   
          buyVolume = state[stock.get_code()]['volume']
          info = '在 %s 以 %s 买入 [%s]%s %s 股' % (str(df_final['date']) + ' ' + str(df_final['time']), price, df_final['code'], df_final['name'], str(buyVolume))
          MyLog.info(info)
          if self.__config.get_t1()['trade']['enable']:
             res = str(self.__trade.buy(df_final['code'],buyVolume,float(price)))
             if 'entrust_no' in res or 'success' in res:
                 stock.set_cache('buy_price',d_price)
          elif self.__config.get_t1()['trade']['enableMock']:
               res = self.__mockTrade.mockTrade(df_final['code'],float(price),buyVolume)
               if res == 0:
                  stock.set_cache('buy_price',d_price)
          return False