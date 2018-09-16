# -*-coding=utf-8-*-
__author__ = 'aqua'

from ..MyLog import MyLog
from sqlalchemy import create_engine
import tushare as ts
import pandas as pd
import numpy as np
import datetime as dt
import time
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

      def calcMain(self,zs,dh,timestamp,balance,lock):
          data = dh.get_data()
          finalCode = ''
          result = []
          codes = []
          for code in data:
              if not self.hasNewData(data[code]):
                 continue 
              if code in dh.get_ignore():
                 continue
            #   self.updateStock(data[code],dh)  
              if code in dh.get_buyed():
                 #self.cancelBuyIfNeed(data[code],dh,timestamp,lock,balance)
                 continue  
              try:  
                 if self.calc(zs,data[code],dh):
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
                     self.outputRes(stock,last_line,timestamp,dh,balance,lock)
                 except Exception as e:
                        MyLog.error('outputRes error %s' % stock.get_code())
                        MyLog.error(str(e))   


      def updateStock(self,stock,dh):
          self.updateBreak10(stock)
          max_amount = stock.get_cache('max_b1_amount') 
          now_line = stock.get_Lastline()
          stop_price = round(float(now_line['pre_close']) * 1.1, 2)
          if float(now_line['b1_p']) == stop_price:
             now_amount = float(now_line['b1_p']) * self.convertToFloat(now_line['b1_v']) * 100  
             if max_amount is None or now_amount > max_amount:
                stock.set_cache('max_b1_amount',now_amount)
          if stock.get_code() in dh.get_buyed():      
             last_second_line = stock.get_LastSecondline()
             if last_second_line is None or float(last_second_line['b1_p']) != stop_price:
                return 
             deal_amount = self.convertToFloat(now_line['amount']) - self.convertToFloat(last_second_line['amount'])   
             old_deal_amount = stock.get_cache('deal_amount')
             if old_deal_amount is None:
                stock.set_cache('deal_amount',[deal_amount])  
             else:
                 if len(old_deal_amount) >= 15:
                    old_deal_amount.pop(0)
                 old_deal_amount.append(deal_amount) 
                 stock.set_cache('deal_amount',old_deal_amount)   


      def cancelBuyIfNeed(self,stock,dh,timestamp,lock,balance):
          trade = self.__config.get_t1()['trade']
          last_second_line = stock.get_LastSecondline()
          now_line = stock.get_Lastline()
          last_second_buy1_v = self.convertToFloat(last_second_line['b1_v']) 
          last_second_buy1_amount = float(last_second_line['b1_p']) * last_second_buy1_v * 100
          now_buy1_v = self.convertToFloat(now_line['b1_v'])
          now_buy1_amount = float(now_line['b1_p']) * now_buy1_v * 100 
          stop_price = round(float(now_line['pre_close']) * 1.1, 2)
          max_b1_amount = stock.get_cache('max_b1_amount')
          deal_amount = self.convertToFloat(now_line['amount']) - self.convertToFloat(last_second_line['amount'])
          cancel_b1_amount = self.__config.get_t1()['hit10']['cancel_b1_amount']
          strTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
          if strTime > '13:30:00':
             cancel_b1_amount = self.__config.get_t1()['hit10']['cancel_b1_amount_1']
          if strTime > '14:30:00':
             cancel_b1_amount = self.__config.get_t1()['hit10']['cancel_b1_amount_2']    
          if max_b1_amount is None:
             max_b1_amount = -1 
          sum_last_10_deal_amount = 0
          last_10_deal_amount = stock.get_cache('deal_amount')   
          if last_10_deal_amount is not None:
             sum_last_10_deal_amount = sum(last_10_deal_amount)
          if float(now_line['price']) == stop_price:
             if float(now_line['b1_p']) == stop_price and self.convertToFloat(now_line['a1_v']) == 0 and (now_buy1_amount < cancel_b1_amount or now_buy1_v < last_second_buy1_v * self.__config.get_t1()['hit10']['cancel_ratio'] or now_buy1_amount < max_b1_amount * self.__config.get_t1()['hit10']['cancel_ratio_max_amount'] or deal_amount >= now_buy1_amount * self.__config.get_t1()['hit10']['cancel_deal_amount_ratio'] or sum_last_10_deal_amount > now_buy1_amount * self.__config.get_t1()['hit10']['max_deal_amount']):
                info = '[%s] 在 [%s] 撤单 [%s],b1_v=%s' % (Utils.getCurrentTime(),str(now_line['date']) + ' ' + str(now_line['time']),stock.get_code(),now_buy1_v)
                MyLog.info(info)
                if trade['enable'] or trade['enableMock']:
                   self.cancelBuy(trade,stock,dh,lock,balance) 
                # self.printPerformace(timestamp)

      @Utils.async   
      def cancelBuy(self,trade,stock,dh,lock,balance):
          status = -1
          if trade['enable']:                    
             try:
                lock.acquire()
                status = self.__trade.cancel(stock.get_code(),True) 
                buyMoney = stock.get_cache('buyMoney')
                if buyMoney is not None:
                   balance.value = balance.value + buyMoney
             except Exception as e:
                    pass
             finally:
                     lock.release()
          if trade['enableMock']:
             buyMoney = stock.get_cache('buyMoney')
             if buyMoney is not None:
                balance.value = balance.value + buyMoney 
             status = self.__mockTrade.cancelBuy(stock.get_code())
          #cancel success
          if status == 0: 
             MyLog.info('[%s] 撤单成功' % stock.get_code()) 
             now_line = stock.get_Lastline()
             now_buy1_v = self.convertToFloat(now_line['b1_v'])
             now_buy1_amount = float(now_line['b1_p']) * now_buy1_v * 100
             stock.set_cache('cancel_b1_amount',now_buy1_amount)
             dh.get_buyed().remove(stock.get_code()) 
          #cancel failed, already buyed   
          else:
              MyLog.info('[%s] 撤单失败' % stock.get_code())
              stock.add_cancelTimes()
              if stock.get_cancelTimes() >= 2:
                 dh.add_ignore(stock.get_code()) 



      @Utils.async
      def outputRes(self,stock,df_final,timestamp,dh,balance,lock):
          d_price = round(float(df_final['pre_close']) * 1.1, 2)
          trade = self.__config.get_t1()['trade']
          buyVolume = trade['volume']
          if trade['dynamicVolume']:
             buyVolume = int(trade['amount'] / d_price / 100) * 100
          buyMoney = d_price * buyVolume  
          price = str('%.2f' % d_price)
          try:
             lock.acquire()
             if buyMoney > balance.value or buyVolume == 0:
                return None   
             if df_final['code'] in dh.get_buyed():
                return None 
             info = '[%s] 在 %s 以 %s 买入 [%s]%s %s 股' % (Utils.getCurrentTime(),str(df_final['date']) + ' ' + str(df_final['time']), price, df_final['code'], df_final['name'], str(buyVolume))
             MyLog.info(info)
             now = dt.datetime.now()
             deltaSeconds = (now - timestamp).seconds
             if deltaSeconds > trade['timestampLimit']:
                MyLog.info('[%s] 行情超时 %s秒 放弃买入' % (df_final['code'],deltaSeconds)) 
                return None
             if trade['enable']:
                res = str(self.__trade.buy(df_final['code'],buyVolume,float(price)))
                if 'entrust_no' in res or 'success' in res:
                   balance.value = balance.value - buyMoney
                   stock.set_cache('buyMoney',buyMoney)
                   dh.add_buyed(df_final['code'])
                   return df_final['code']
                return None
             if trade['enableMock']:
                res = self.__mockTrade.mockTrade(df_final['code'],float(price),buyVolume)
                if res == 0:
                   balance.value = balance.value - buyMoney
                   stock.set_cache('buyMoney',buyMoney)
                   dh.add_buyed(df_final['code'])
                   return df_final['code']
                return None  
             dh.add_buyed(df_final['code'])  
             return df_final['code']  
          except Exception as e:
                 return None
          finally:
                  lock.release()  
                #   self.printPerformace(timestamp)


              
      def calc(self,zs,stock,dh):
          if not self.canCalc(stock,dh):
             return False
          return self.isStockMatch(zs,stock,dh)   

      def isOpenMatch(self,row):
          if float(row['pre_close']) == 0 or float(row['open']) == 0:
             return False
          return (float(row['open']) - float(row['pre_close'])) / float(row['pre_close']) * 100 >= -1.5


      def hasNewData(self,stock):
          lastLine = stock.get_Lastline()
          if stock.get_time() == lastLine['time']:
             return False
          stock.set_time(lastLine['time'])  
          return True


      def canCalc(self,stock,dh):
          if stock.len() < 2:
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


      def isStockMatch(self,zs,stock,dh):
          if self.isZSMatch(zs,stock):
             return self.isYDLS(stock)


      def get_data_time(self,data):
          return dt.datetime.strptime(data['date'] + ' ' + data['time'],'%Y-%m-%d %H:%M:%S')      


      def isYDLS(self, stock):
          now_line = stock.get_Lastline()  
          if float(now_line['high']) >= float(now_line['price']):
             return False
          stop_p = self.__config.get_t1()['ydls']['stop_p']
          current_p = self.getCurrentPercent(stock)
          if current_p < stop_p[0] or current_p > stop_p[1]:
             return False
          if self.getOpenPercent(stock) - self.getPercent(now_line['low'],stock) > self.__config.get_t1()['ydls']['open-low']:
             return False
          datas = stock.get_data_in_len(self.__config.get_t1()['ydls']['in_len'])
          length = len(datas)
          last_datetime = self.get_data_time(datas[-1])
          fist_datetime = self.get_data_time(datas[-1 * length])
          p = self.getPercent(datas[-1]['price'],stock) - self.getPercent(datas[-1 * length]['price'],stock)
          amount = self.convertToFloat(datas[-1]['amount']) - self.convertToFloat(datas[-1 * length]['amount'])
          if (last_datetime - fist_datetime).seconds < 60:
             if p < self.__config.get_t1()['ydls']['yd_p']:
                return False
             if amount < self.__config.get_t1()['ydls']['yd_amount']:
                return False 
             return True   
          else:
               if length > 20:
                  step = 5
                  i = -20
                  while i >= length * -1:
                        p = self.getPercent(datas[-1]['price'],stock) - self.getPercent(datas[i]['price'],stock)
                        amount = self.convertToFloat(datas[-1]['amount']) - self.convertToFloat(datas[i]['amount'])
                        fist_datetime_temp = self.get_data_time(datas[i])
                        i = i - step
                        if (last_datetime - fist_datetime_temp).seconds < 60:
                           continue 
                        if p >= pow(((last_datetime - fist_datetime_temp).seconds - 60),self.__config.get_t1()['ydls']['yd_ratio']) + self.__config.get_t1()['ydls']['yd_p']:
                           if p >= pow(((last_datetime - fist_datetime_temp).seconds - 60),self.__config.get_t1()['ydls']['amount_ratio']) + self.__config.get_t1()['ydls']['yd_amount']:
                              return True 
               if p >= pow(((last_datetime - fist_datetime).seconds - 60),self.__config.get_t1()['ydls']['yd_ratio']) + self.__config.get_t1()['ydls']['yd_p']:
                  if amount >= pow(((last_datetime - fist_datetime).seconds - 60),self.__config.get_t1()['ydls']['amount_ratio']) + self.__config.get_t1()['ydls']['yd_amount']:
                     return True
          return False                  

                    



      def updateBreak10(self,stock):
          if stock.get_cache('status') == 1:
             if stock.get_cache('min_break') is None:
                stock.set_cache('min_break',self.getCurrentPercent(stock))
             elif self.getCurrentPercent(stock) < stock.get_cache('min_break'):
                  stock.set_cache('min_break',self.getCurrentPercent(stock))        

      def isReach10Again(self,stock):
          now_line = stock.get_Lastline()
          stop_price = round(float(now_line['pre_close']) * 1.1, 2)
          if float(now_line['b1_p']) == stop_price and self.convertToFloat(now_line['a1_v']) == 0:
             stock.set_cache('min_break',None)
             stock.set_cache('status',None) 
             return False
          else:
              if self.convertToFloat(now_line['a5_v']) != 0:
                 return False
              if stock.get_cache('min_break') is None or stock.get_cache('min_break') > self.__config.get_t1()['hit10']['min_break']:
                 return False
              if stock.get_cache('break_time') is None or (dt.datetime.now() - stock.get_cache('break_time')).seconds > self.__config.get_t1()['hit10']['break_time']:      
                 return False
              if stock.get_cache('hit_top_time') is None or (stock.get_cache('break_time') - stock.get_cache('hit_top_time')).seconds < self.__config.get_t1()['hit10']['hit_break_inter']:
                 return False   
              total_sell = 0
              for i in range(1,6):
                  total_sell += self.convertToFloat(now_line['a' + str(i) + '_v']) * self.convertToFloat(now_line['a' + str(i) + '_p']) * 100
              if total_sell > stock.get_cache('max_b1_amount') * self.__config.get_t1()['hit10']['max_b1_amount_ratio']:
                 return False       
              info = '[%s]在[%s][%s] match 10,b1_v=%s' % (Utils.getCurrentTime(),str(now_line['date']) + ' ' + str(now_line['time']),stock.get_code(),now_line['b1_v'])
              MyLog.info(info)
              return True
               


      def isbreak10(self,stock,dh):
          now_line = stock.get_Lastline()
          stop_price = round(float(now_line['pre_close']) * 1.1, 2)
          if float(now_line['b1_p']) != stop_price and self.convertToFloat(now_line['a1_v']) != 0:
             count = stock.get_cache('break_count')
             if count is None:
                count = 1 
             else:
                 count = count + 1
             stock.set_cache('break_count',count) 
             if count >= self.__config.get_t1()['hit10']['break_count']:
                stock.set_cache('status',0)
                dh.add_ignore(stock.get_code())
             else:
                  stock.set_cache('break_time',dt.datetime.now())
                  stock.set_cache('min_break',self.getCurrentPercent(stock))
                  stock.set_cache('status',1)  
                  MyLog.info('%s is break 10' % stock.get_code())
          return False         
              

      def isReach10(self,stock):
          now_line = stock.get_Lastline()
          stop_price = round(float(now_line['pre_close']) * 1.1, 2)
          if float(now_line['b1_p']) == stop_price and self.convertToFloat(now_line['a1_v']) == 0:
             hit_top_time = stock.get_cache('hit_top_time')
             strTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
             if hit_top_time is None and strTime > self.__config.get_t1()['hit10']['hit_top_time']:
                return False 
             stock.set_cache('hit_top_time',dt.datetime.now())
             now_b1_amount = self.convertToFloat(now_line['b1_v']) * float(now_line['b1_p']) * 100 
             if now_b1_amount >= self.__config.get_t1()['hit10']['buy_b1_amount']: 
                MyLog.info('%s is reach 10' % stock.get_code()) 
                stock.set_cache('status',0) 
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
          return p > 0.0


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


              


              
