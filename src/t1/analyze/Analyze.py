# -*-coding=utf-8-*-
__author__ = 'aqua'

from ..MyLog import MyLog
import pandas as pd
import numpy as np
import datetime as dt
import cmath
import sys
sys.path.append('../..')
from config.Config import Config 

class Analyze(object):
    
      def __init__(self):
          self.__config = Config()
 
      def calcMain(self,dh):
          data = dh.get_data()
          result = []
          for code in data:
              if self.calc(data[code]):
                 result.append(data[code])
          df_res = self.goTopsis(result)
          print(df_res)


      def goTopsis(self,result):
          df = pd.DataFrame()
          for stock in result:
              self.buildData(df,stock)
          return self.topsisCalc(df)    


      def topsisCalc(self,df):
          df = df.fillna(df.mean())   
          self.commonCalc(df,'net',self.__config.get_t1()['topsis']['net'],True)
          self.commonCalc(df,'speed_near',self.__config.get_t1()['topsis']['speed_near'],True)
          self.commonCalc(df,'speed_total',self.__config.get_t1()['topsis']['speed_total'],True)
          self.commonCalc(df,'bigMoney_amount',self.__config.get_t1()['topsis']['bigMoney_amount'],True)
          self.commonCalc(df,'bigMoney_volume',self.__config.get_t1()['topsis']['bigMoney_volume'],True)    
          self.commonCalc(df,'r_break',self.__config.get_t1()['topsis']['r_break'],False)
          for index,row in df.iterrows():
              self.calcDi(df,index,row,['net','speed_near','speed_total','bigMoney_amount','bigMoney_volume','r_break'],'_best')
              self.calcDi(df,index,row,['net','speed_near','speed_total','bigMoney_amount','bigMoney_volume','r_break'],'_worst')
              self.calcCi(index,row)  
          df = df.sort_values('ci',ascending=False)  
          return df  

      def calcCi(self,df,index,row):
          if (row['Di_best'] + row['Di_worst']) == 0:
             row['ci'] = 0 
             df.loc[index,'ci'] = 0
          else:    
             row['ci'] = row['Di_worst'] / (row['Di_best'] + row['Di_worst'])  
             df.loc[index,'ci'] = row['ci']     


      def calcDi(self,df,index,row,columnList,best_worst):
          temp = 0
          for column in columnList:
              temp = temp + np.square(row[column + '_vi'] - row[column + best_worst])
          row['Di' + best_worst] = cmath.sqrt(temp)
          df.loc[index,'Di' + best_worst] = row['Di' + best_worst] 
 

      def commonCalc(self,df,columnName,weight,positive):
          temp = cmath.sqrt((df[columnName] * df[columnName]).sum())  
          #wi*ri
          if temp == 0:
             df[columnName + '_vi'] = weight * 0
          else:
             df[columnName + '_vi'] = weight * df[columnName] / temp
          #vi+, vi-
          if positive == True:
             df[columnName + '_best'] = df[columnName + '_vi'].max()
             df[columnName + '_worst'] = df[columnName + '_vi'].min()
          else:          
             df[columnName + '_best'] = df[columnName + '_vi'].min()
             df[columnName + '_worst'] = df[columnName + '_vi'].max()           

 
      def buildData(self,df,stock):
          last_line = stock.get_Lastline()
          last_line['net'] = stock.get_net()
          last_line['speed_near'] = stock.get_near_speed()
          last_line['speed_total'] = stock.get_total_speed()
          last_line['bigMoney_amount'] = stock.getBigMoneyTotalAmount()
          last_line['bigMoney_volume'] = stock.getBigMoneyTotalVolume()
          minR = stock.get_minR()
          times = 0
          for i in [1,2,3,4]:
              if 'R' + i != minR:
                  times = times + stock.get_rBreakTimes('R' + i)
              else:
                  break 
          last_line['r_break'] = times
          pd.append(last_line)
          

              
      def calc(self,stock):
          MyLog.info('=== ' + stock.get_code() + " ===\n")
          MyLog.info(stock.get_data())
          if not self.canCalc(stock):
             return False 
          open_p = self.getOpenPercent(stock)
          conf = self.getConfig(open_p)  
          self.initStockData(stock,open_p,conf)
          self.updateStock(stock,conf)  
          return self.isStockMatch(stock,conf)   


      def canCalc(self,stock):
          if stock.len() < 0:
             return False
          lastLine = stock.get_Lastline() 
          if lastLine.get('open') == 0.0:
             return False
          lastSecondLine = stock.get_LastSecondline() 
          if lastSecondLine.get('open') == 0.0:
             return False    
          return True     


      def initStockData(self,stock,open_p,conf):
          r_line = self.__config.get_t1()['R_line']
          for key in r_line:
              val = open_p + (10 - open_p) * r_line[key]
              stock.set_r_val(key,val)


      def updateStock(self,stock,conf):
          self.updateBreakRtimes(stock,conf)
          self.updateSpeedCount(stock,conf)
          self.updateBigMoney(stock,conf)



      def updateSpeedCount(self,stock,conf):
          data = stock.get_data()
          last_line = data.iloc[-1]
          pre_pos = conf['speed']['near_pos']
          if pre_pos > stock.len():
             pre_pos = stock.len() 
          df_temp = data.tail(pre_pos)
          for index,row in df_temp.iterrows():
              if row['open'] != 0:
                 p = (float(last_line.get('price')) - float(row['price'])) / float(row['open']) * 100 
                 stock.set_near_speed(p)
                 break
          last_second_line = data.iloc[-2]
          p = (float(last_line.get('price')) - float(last_second_line.get('price'))) / float(last_line.get('open')) * 100 
          if p > conf['speed']['min_single_p']:
             stock.add_total_speed(p)      


      def theLastIsSellOrBuy(self,stock):
          lastLine = stock.get_Lastline()
          lastSeconfLine = stock.get_LastSecondline()
          last_amount = float(lastLine.get('amount'))
          last_sec_amount = float(lastSeconfLine.get('amount'))
          if last_sec_amount == last_amount:
             return 'no_deal' 
          last_price = float(lastLine.get('price'))  
          last_b_p_1 = float(lastLine.get('b1_p'))
          last_b_v_1 = float(lastLine.get('b1_v'))
          last_a_p_1 = float(lastLine.get('a1_p'))
          last_a_v_1 = float(lastLine.get('a1_v'))
          last_sec_price = float(lastSeconfLine.get('price'))
          last_sec_b_p_1 = float(lastSeconfLine.get('b1_p'))
          last_sec_b_v_1 = float(lastSeconfLine.get('b1_v'))
          last_sec_a_p_1 = float(lastSeconfLine.get('a1_p'))
          last_sec_a_v_1 = float(lastSeconfLine.get('a1_v'))
          if (last_a_p_1 > last_sec_a_p_1 or (last_a_p_1 == last_sec_a_p_1 and last_a_v_1 < last_sec_a_v_1)) and (last_price >= last_sec_price):
             return 'drive_buy'
          elif (last_b_p_1 < last_sec_b_p_1 or (last_b_p_1 == last_sec_b_p_1 and last_b_v_1 < last_sec_b_v_1)) and (last_price <= last_sec_price):
             return 'drive_sell'
          return 'unknown'       


      def updateBigMoney(self,stock,conf):
          lastLine = stock.get_Lastline()
          lastSeconfLine = stock.get_LastSecondline()
          last_amount = float(lastLine.get('amount'))
          last_sec_amount = float(lastSeconfLine.get('amount'))
          last_volume = float(lastLine.get('volume'))
          last_sec_volume = float(lastSeconfLine.get('volume'))
          amount = last_amount - last_sec_amount
          volume = last_volume - last_sec_volume
          if amount >= conf['big_money']['single_amount']:
             stock.addBigMoneyTotalAmount(amount)
          if volume >= conf['big_money']['single_volume']:
             stock.addBigMoneyTotalVolume(volume) 
          type = self.theLastIsSellOrBuy(stock)
          if type == 'drive_buy':
             stock.addNetBuy(last_amount - last_sec_amount)  
          elif type == 'drive_sell':
             stock.addNetBuy(last_sec_amount - last_amount)           

             
      def updateBreakRtimes(self,stock,conf):
          now_p = self.getCurrentPercent(stock)
          lastSecondLine = stock.get_LastSecondline()
          last_p = self.getPercent(lastSecondLine.get('price'),stock)
          for key in ['R1','R2','R3','R4','R5']:
              val = stock.get_r_val(key)
              if last_p > val and now_p < val:
                 stock.add_rBreakTimes(key) 
          minR = conf['min_R']
          if stock.get_rBreakTimes(minR) > 0:
             for i in [1,2,3,4,5]:
                 if i > int(minR[-1]) and stock.get_rBreakTimes('R' + i) == 0:
                    stock.set_minR('R' + i)        
          else:
              stock.set_minR(minR)



      def getConfig(self,open_p):
          t1 = self.__config.get_t1()
          keys = ['A','B','C','D']
          for key in keys:
              if t1[key]['open_p'][0] and open_p < t1[key]['open_p'][1]:
                 return t1[key] 

      def isStockMatch(self,stock,conf):
          if not self.isTimeMatch(conf):
             return False
          if not self.isReachMinR(stock):
             return False
          if not self.isNetMatch(stock,conf):
             return False      
          if stock.get_minR() != 'R5':
             if not self.isPeedMatch(stock,conf) and not self.isBigMoneyMatch(stock,conf):
                return False 
          return self.isLastTwoMatch(stock)


      def isLastTwoMatch(self,stock):
          now_p = self.getCurrentPercent(stock)
          lastSecondLine = stock.get_LastSecondline()
          last_p = self.getPercent(lastSecondLine.get('price'),stock)
          return now_p > 0 and last_p >= 0
          


      def isPeedMatch(self,stock,conf):
          stock.get_near_speed() >= conf['speed']['threshold'] or stock.get_total_speed() >= conf['speed']['threshold']


      def isBigMoneyMatch(self,stock,conf):
          stock.getBigMoneyTotalAmount() >= conf['big_money']['total_amount'] or stock.getBigMoneyTotalVolume() >= conf['big_money']['total_volume']


      def isNetMatch(self,stock):
          return stock.get_net() >= conf['big_money']['net']



      def isTimeMatch(self,conf):
          now = dt.datetime.now()
          timeStr = now.strftime('%H:%M:%S')
          return timeStr <= conf['time']


      def getPercent(self,price,stock):
          lastLine = stock.get_Lastline()
          pre_close = lastLine.get('pre_close') 
          open_p = (price - pre_close) / pre_close * 100
          return open_p
      
      def getCurrentPercent(self,stock):
          lastLine = stock.get_Lastline()
          price = lastLine.get('price')
          return self.getPercent(price,stock)
              

      def getOpenPercent(self,stock):
          lastLine = stock.get_Lastline()
          open = lastLine.get('open')
          return self.getPercent(open,stock)  


      def isReachMinR(self,stock):
          now_p = self.getCurrentPercent(stock)
          minR = stock.get_minR()
          return now_p > stock.get_r_val(minR)

              


              
