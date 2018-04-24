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

class NewAnalyze(object):
    
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

      def calcMain(self,dh,timestamp,buyCount):
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
                     res = self.outputRes(last_line,timestamp,buyCount)
                     if res is not None:
                        codes.append(stock.get_code())
                 except Exception as e:
                        MyLog.error('outputRes error %s' % stock.get_code())
                        MyLog.error(str(e))   
          return codes   


      def outputRes(self,df_final,timestamp,buyCount):
          trade = self.__config.get_t1()['trade']
          if buyCount <= 0:
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
          if not self.canCalc(stock,dh):
             return False 
          open_p = self.getOpenPercent(stock)
          conf = self.getConfig(open_p)  
          if conf is None:
             dh.add_ignore(stock.get_code()) 
             return False 
          if not stock.is_inited():  
             self.initStockData(stock,open_p,conf)
          self.updateStock(stock,conf)  
          return self.isStockMatch(stock,conf,dh)   


      def isOpenMatch(self,row):
          if float(row['pre_close']) == 0 or float(row['open']) == 0:
             return False
          return (float(row['open']) - float(row['pre_close'])) / float(row['pre_close']) * 100 >= -1.0


      def canCalc(self,stock,dh):
          if stock.len() < 0:
             return False
          lastLine = stock.get_Lastline() 
          if float(lastLine['open']) == 0.0:
             return False
          lastSecondLine = stock.get_LastSecondline()
          if lastSecondLine is None:
             return False  
          if float(lastSecondLine['open']) == 0.0:
             return False    
          return True     


      def initStockData(self,stock,open_p,conf):
          r_line = self.__config.get_t1()['R_line']
          for key in r_line:
              if stock.get_r_val(key) == -10:
                 val = open_p + (10 - open_p) * r_line[key]
                 stock.set_r_val(key,val)
          stock.set_inited()       

      def updateStock(self,stock,conf):
          self.updateBreakRtimes(stock,conf)


      def convertToFloat(self,str):
          if str == '':
             return 0 
          try:
              return float(str)
          except Exception as e:
                 MyLog.error('convertToFloat error: ' + str + '\n') 
                 return 0   


      def updateBreakRtimes(self,stock,conf):
          now_p = self.getCurrentPercent(stock)
          lastSecondLine = stock.get_LastSecondline()
          last_p = self.getPercent(lastSecondLine['price'],stock)
          for key in ['R1','R2','R3','R4']:
              val = stock.get_r_val(key)
              if last_p > val and now_p < val:
                 stock.add_rBreakTimes(key) 
          minR = stock.get_minR()
          if minR is None:
             minR = conf['min_R']
          if stock.get_rBreakTimes(minR) > 0:
             for i in [1,2,3,4,5]:
                 if i > int(minR[-1]) and stock.get_rBreakTimes('R' + str(i)) == 0:
                    stock.set_minR('R' + str(i))
                    break        
          else:
              stock.set_minR(minR)



      def getConfig(self,open_p):
          t1 = self.__config.get_t1()
          keys = ['A','B','C']
          for key in keys:
              if t1[key]['open_p'][0] <= open_p and open_p < t1[key]['open_p'][1]:
                 return t1[key] 

      def isStockMatch(self,stock,conf,dh):
          if 'time' in self.__config.get_t1()['strategy'] and not self.isTimeMatch(stock,conf):
             return False
          if 'xspeed' in self.__config.get_t1()['strategy'] and not self.isXSpeedMatch(dh,stock):
             return False
          if 'sellWindow' in self.__config.get_t1()['strategy'] and not self.isSellWindowMatch(stock):
             return False 
          if 'minR' in self.__config.get_t1()['strategy'] and not self.isReachMinR(stock):
             return False   
          return self.isLastTwoMatch(stock)


      def isSellWindowMatch(self,stock):
          data = stock.get_data()
          size = len(data)
          if size > self.__config.get_t1()['big_money']['count']:
             size = self.__config.get_t1()['big_money']['count'] 
          data = data[size * -1:]
          count = 0
          lastAmount = None
          for row in data: 
              nowAmount = self.convertToFloat(row['amount'])   
              if lastAmount is not None and (nowAmount - lastAmount >= self.__config.get_t1()['big_money']['amount']):
                 count = count + 1
              lastAmount = nowAmount
          if (count / size < self.__config.get_t1()['big_money']['threshold']):
             return False         
          now_line = stock.get_Lastline()
          limit_v = self.__config.get_t1()['sellWindow']['volume']
          return self.convertToFloat(now_line['a1_v']) < limit_v and self.convertToFloat(now_line['a2_v']) < limit_v and self.convertToFloat(now_line['a3_v']) < limit_v and self.convertToFloat(now_line['a4_v']) < limit_v and self.convertToFloat(now_line['a5_v']) < limit_v  


      def isXSpeedMatch(self,dh,stock):
          now_line = stock.get_Lastline() 
          ccp = self.getCurrentPercent(stock)
          ocp = self.getOpenPercent(stock)
          if ocp - ccp >= self.__config.get_t1()['x_speed']['lowerThanBefore']:
             stock.add_lowerThanBeforeTimes()
             if stock.get_lowerThanBeforeTimes() > self.__config.get_t1()['x_speed']['lowerThanBeforeTimes']: 
                dh.add_ignore(stock.get_code()) 
                return False 
          ct = dt.datetime.strptime(now_line['date'] + ' ' + now_line['time'], '%Y-%m-%d %H:%M:%S')
          pcpArray = self.generatePCPArray(stock)
          i = 0
          while i < len(pcpArray):
                line = pcpArray[i] 
                if line['time'] == now_line['time']:
                   break 
                price = float(line['price'])    
                pcp = (float(pcpArray[i]['price']) - float(pcpArray[i]['pre_close'])) / float(pcpArray[i]['pre_close']) * 100 
                if pcp - ccp >= self.__config.get_t1()['x_speed']['lowerThanBefore']:
                   stock.add_lowerThanBeforeTimes() 
                   if stock.get_lowerThanBeforeTimes() > self.__config.get_t1()['x_speed']['lowerThanBeforeTimes']: 
                      dh.add_ignore(stock.get_code()) 
                      return False  
                if ccp - pcp >= (10 - pcp) * self.__config.get_t1()['x_speed']['a']:
                   if ccp - pcp >= (ccp - ocp) * self.__config.get_t1()['x_speed']['b'] and pcp > ocp:
                      pt = dt.datetime.strptime(line['date'] + ' ' + line['time'], '%Y-%m-%d %H:%M:%S')
                      if (ct - pt).seconds / 60 < (ccp - pcp) * self.__config.get_t1()['x_speed']['c']:
                          MyLog.info('[%s] match cond a, ccp = %s, pcp = %s' % (stock.get_code(),ccp,pcp)) 
                          MyLog.info('[%s] match cond b, ccp = %s, ocp = %s' % (stock.get_code(),ccp,ocp)) 
                          MyLog.info('[%s] match cond c, ct = %s, pt = %s' % (stock.get_code(),ct,pt))
                          last_second_line = stock.get_LastSecondline()
                          stock.add_buySignal()
                          if stock.get_buySignal() >= self.__config.get_t1()['trade']['maxBuySignal']:
                             return True
                          return False  
                i = i + 1 
        #   stock.reset_buySignal()   
          return False  


      def generatePCPArray(self,stock):
          pcpArray = []
          len = stock.len()
          start = 0
          step = 1
          if len > 30:
             if len > 250:
                start = -250 
                len = 250  
             step = math.ceil(len / 30)
          data = stock.get_data()
          for val in data[start::step]:
              pcpArray.append(val)
          return pcpArray    
                                    
                   

      def isLastTwoMatch(self,stock):
          data = stock.get_data()
          if stock.len() < 3:
             return False 
          price = float(data[-1]['price'])
          price2 = float(data[-2]['price'])
          price3 = float(data[-2]['price']) 
          return price - price2 >= 0 and price2 - price3 >= 0
          


      def isTimeMatch(self,stock,conf):
          lastLine = stock.get_Lastline()
          timeStr = lastLine['time']
          return timeStr <= conf['time']


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


      def isReachMinR(self,stock):
          now_p = self.getCurrentPercent(stock)
          minR = stock.get_minR()
          return now_p > stock.get_r_val(minR)

              


              
