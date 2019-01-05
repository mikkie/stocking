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

      def calcMain(self,zs,dh,balance):
          data = dh.get_data()
          for code in data:
              if len(dh.get_selled()) > 0:
                 if code in dh.get_selled():
                    continue 
              try:  
                 if self.calc(zs,data[code],dh,balance):
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
          now_line = stock.get_Lastline()
          buy_price = stock.get_cache('buy_price')
          if buy_price is None:
             buy_price = self.__config.get_t1()['seller'][stock.get_code()]['price']
             stock.set_cache('buy_price',buy_price)  
          return (self.convertToFloat(now_line['price']) - buy_price) / buy_price * 100
              

      def getOpenPercent(self,stock):
          lastLine = stock.get_Lastline()
          open = lastLine.get('open')
          return self.getPercent(open,stock)                


      def initLS(self,stock,dh,ratio):
          ccp = self.getWinLossPercent(stock)
          ls = ccp - self.__config.get_t1()['seller'][stock.get_code()]['margin'] * ratio
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


      def is_force_bc(self, stock):
          bc_force_p = self.__config.get_t1()['seller']['bc_force_p']
          now_line = stock.get_Lastline()
          now_price = self.convertToFloat(now_line['price'])
          current_p = self.getCurrentPercent(stock)
          if current_p < bc_force_p:
             lowest_price = self.convertToFloat(now_line['low'])
             if now_price != lowest_price and (now_price - lowest_price) / self.convertToFloat(now_line['pre_close']) * 100 < self.__config.get_t1()['seller'][stock.get_code()]['p_limit_lowest']:
                MyLog.info('force bc match, time = %s, p = %s' % (now_line['date'] + ' ' + now_line['time'], current_p))
                return True
          return False


      def is_bc_point(self, stock):
          now_line = stock.get_Lastline()
          now_price = self.convertToFloat(now_line['price'])
          lowest_price = self.convertToFloat(now_line['low'])
          if now_price == lowest_price or (now_price - lowest_price) / self.convertToFloat(now_line['pre_close']) * 100 > self.__config.get_t1()['seller'][stock.get_code()]['p_limit_lowest']:
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
          tag = amount > self.__config.get_t1()['seller'][stock.get_code()]['min_amount'] and amount_ratio > self.__config.get_t1()['seller'][stock.get_code()]['amount_ratio'] 
          if tag:
             MyLog.info('bc buy match: time = %s, lowest_price = %s, buy_amount = %s, sell_amount = %s, amount_ratio = %s' % (now_line['date'] + ' ' + now_line['time'], lowest_price, amount, sell_amount, amount_ratio)) 
          return tag


      def is_bc_sell(self, stock):
          now_line = stock.get_Lastline()
          buy_price = stock.get_cache('bc_buy_price')
          if buy_price is None:
             return False 
          if (self.convertToFloat(now_line['price']) - buy_price) / buy_price * 100 >= self.__config.get_t1()['seller'][stock.get_code()]['bc_sell_profit']:
             return True 
          return False


      def is_ydxd(self, stock):
          now_line = stock.get_Lastline()
          datas = stock.get_data()
          now_price = self.convertToFloat(datas[-1]['price'])
          lowest_price = self.convertToFloat(datas[-1]['low'])
          start = -20
          if len(datas) < 20:
             start = len(datas) * -1
          temp = datas[start:]
          high = None
          for row in temp:
              price = self.convertToFloat(row['price'])
              if high is None or price > high:
                 high = price
          ydxd = (high - now_price) / self.convertToFloat(datas[-1]['pre_close']) * 100
          if ydxd < self.__config.get_t1()['seller'][stock.get_code()]['ydxd']:
             return False
          if now_price == lowest_price or (now_price - lowest_price) / self.convertToFloat(datas[-1]['pre_close']) * 100 > self.__config.get_t1()['seller'][stock.get_code()]['p_limit_lowest']:
             return False
          MyLog.info('ydxd match: time = %s, p = %s' % (now_line['date'] + ' ' + now_line['time'], ydxd))  
          return True   


                     



      def calc(self,zs,stock,dh,balance):
          if stock.get_cache('bc_buy_price') is not None:
             if self.is_bc_sell(stock):
                sellVolume = self.__config.get_t1()['seller'][stock.get_code()]['volume'] 
                now = dt.datetime.now()
                check_bc_buy_time = stock.get_cache('check_bc_buy_time')
                if check_bc_buy_time is None or (now - check_bc_buy_time).seconds >= 30:
                   stock.set_cache('check_bc_buy_time', now) 
                   if self.__config.get_t1()['trade']['enable']:
                      if self.__trade.has_bc_buy(stock.get_code(), sellVolume):
                         return self.sell(stock, sellVolume)
                   if self.__config.get_t1()['trade']['enableMock']:
                      if self.__mockTrade.has_buy(stock.get_code(), sellVolume):
                         return self.sell(stock, sellVolume)       
             return False
          ratio = 1
          my_stop_loss = self.__config.get_t1()['seller'][stock.get_code()]['my_loss']
          stop_loss = self.__config.get_t1()['seller'][stock.get_code()]['loss']
          stop_win = self.__config.get_t1()['seller'][stock.get_code()]['win']
          enable_bc = self.__config.get_t1()['seller'][stock.get_code()]['enable_bc']
          if enable_bc and self.getWinLossPercent(stock) < my_stop_loss:
             now_line = stock.get_Lastline()
             if now_line['time'] > '14:30:00':
                return False
             if self.is_force_bc(stock) or (self.getCurrentPercent(stock) < stop_loss and self.is_bc_point(stock)) or self.is_ydxd(stock):
                return self.bc_buy(stock,balance)  
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
             if stock.get_sellSignal() > self.__config.get_t1()['seller']['maxSellSignal'] and self.getCurrentPercent(stock) >= self.__config.get_t1()['seller'][stock.get_code()]['win']: 
                amount = self.__config.get_t1()['seller'][stock.get_code()]['sell_volume']
                return self.sell(stock, amount=amount)
             return False
          else:
               stock.reset_sellSignal()
               ccp = self.getWinLossPercent(stock)
               tls = ccp - self.__config.get_t1()['seller'][stock.get_code()]['margin'] * ratio
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


      def sell(self,stock, amount=None):
          if not self.can_sell(stock):
             return False 
          last_line = stock.get_Lastline()
          price = float(str('%.2f' % (float(last_line['price']))))
          info = '[%s] 在 %s 以 %s 卖出 [%s]%s 全部股票' % (Utils.getCurrentTime(),str(last_line['date']) + ' ' + str(last_line['time']), price, last_line['code'], last_line['name'])
          MyLog.info(info)
          if self.__config.get_t1()['trade']['enable']:
             tag = self.__trade.sell(stock.get_code(),price, amount = amount)
             if amount is not None:
                return True
             return tag  
          elif self.__config.get_t1()['trade']['enableMock']:
               tag = self.__mockTrade.sell(stock.get_code(),price, amount = amount)
               if amount is not None:
                  return True
               return tag 
          return True


      def bc_buy(self, stock, balance):
          df_final = stock.get_Lastline()     
          d_price = round(float(df_final['price']), 2)
          price = str('%.2f' % d_price)
          buyVolume = self.__config.get_t1()['seller'][stock.get_code()]['volume']
          buyMoney = d_price * buyVolume
          if balance is not None and buyMoney > balance.value or buyVolume == 0:
             return False
          info = '在 %s 以 %s 买入 [%s]%s %s 股' % (str(df_final['date']) + ' ' + str(df_final['time']), price, df_final['code'], df_final['name'], str(buyVolume))
          MyLog.info(info)
          if self.__config.get_t1()['trade']['enable']:
             res = str(self.__trade.buy(df_final['code'],buyVolume,float(price)))
             if 'entrust_no' in res or 'success' in res:
                 stock.set_cache('bc_buy_price',d_price)
          elif self.__config.get_t1()['trade']['enableMock']:
               res = self.__mockTrade.mockTrade(df_final['code'],float(price),buyVolume)
               if res == 0:
                  stock.set_cache('bc_buy_price',d_price)
          stock.set_cache('bc_buy_price',d_price)        
          return False