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
          if len(result) != 0:
             df_res = self.goTopsis(result)
             print(df_res)


      def goTopsis(self,result):
          df = pd.DataFrame()
          for stock in result:
              df = self.buildData(df,stock)
          return self.topsisCalc(df)    


      def topsisCalc(self,df):
          df = df.fillna(df.mean())   
          self.commonCalc(df,'net',self.__config.get_t1()['topsis']['net'],True)
          self.commonCalc(df,'speed_near',self.__config.get_t1()['topsis']['speed_near'],True)
          self.commonCalc(df,'speed_total',self.__config.get_t1()['topsis']['speed_total'],True)
          self.commonCalc(df,'s40',self.__config.get_t1()['topsis']['s40'],True)
          self.commonCalc(df,'s100',self.__config.get_t1()['topsis']['s100'],True)
          self.commonCalc(df,'s10',self.__config.get_t1()['topsis']['s10'],True)
          self.commonCalc(df,'bigMoney_amount',self.__config.get_t1()['topsis']['bigMoney_amount'],True)
          self.commonCalc(df,'bigMoney_volume',self.__config.get_t1()['topsis']['bigMoney_volume'],True)    
          self.commonCalc(df,'r_break',self.__config.get_t1()['topsis']['r_break'],False)
          for index,row in df.iterrows():
              self.calcDi(df,index,row,['net','speed_near','speed_total','s40','s100','s10','bigMoney_amount','bigMoney_volume','r_break'],'_best')
              self.calcDi(df,index,row,['net','speed_near','speed_total','s40','s100','s10','bigMoney_amount','bigMoney_volume','r_break'],'_worst')
              self.calcCi(df,index,row)  
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
          data = stock.get_data()
          last_line = stock.get_Lastline()
          data.loc[data['time'] == last_line['time'], 'net'] = stock.get_net()
          data.loc[data['time'] == last_line['time'], 'speed_near'] = stock.get_near_speed()
          data.loc[data['time'] == last_line['time'], 'speed_total'] = stock.get_total_speed()
          data.loc[data['time'] == last_line['time'], 's100'] = stock.get_speed('s100')
          data.loc[data['time'] == last_line['time'], 's40'] = stock.get_speed('s40')
          data.loc[data['time'] == last_line['time'], 's10'] = stock.get_speed('s10')
          data.loc[data['time'] == last_line['time'], 'bigMoney_amount'] = stock.getBigMoneyTotalAmount()
          data.loc[data['time'] == last_line['time'], 'bigMoney_volume'] = stock.getBigMoneyTotalVolume()
          minR = stock.get_minR()
          times = 0
          for i in [1,2,3,4]:
              if 'R' + str(i) != minR:
                  times = times + stock.get_rBreakTimes('R' + str(i))
              else:
                  break 
          data.loc[data['time'] == last_line['time'], 'r_break'] = times
          last_line = stock.get_Lastline()
          return df.append([last_line])
          

              
      def calc(self,stock):
          MyLog.info('=== ' + stock.get_code() + " ===\n")
          if not self.canCalc(stock):
             return False 
          open_p = self.getOpenPercent(stock)
          conf = self.getConfig(open_p)  
          if conf is None:
             return False 
          self.initStockData(stock,open_p,conf)
          self.updateStock(stock,conf)  
          return self.isStockMatch(stock,conf)   


      def canCalc(self,stock):
          if stock.len() < 0:
             return False
          lastLine = stock.get_Lastline() 
          if float(lastLine.get('open')) == 0.0:
             return False
          lastSecondLine = stock.get_LastSecondline() 
          if float(lastSecondLine.get('open')) == 0.0:
             return False    
          return True     


      def initStockData(self,stock,open_p,conf):
          r_line = self.__config.get_t1()['R_line']
          for key in r_line:
              if stock.get_r_val(key) == -10:
                 val = open_p + (10 - open_p) * r_line[key]
                 stock.set_r_val(key,val)


      def updateStock(self,stock,conf):
          self.updateBreakRtimes(stock,conf)
          self.updateSpeedCount(stock,conf)
          try:
             self.updateBigMoney(stock,conf)
          except Exception as e:
                 MyLog.error('updateBigMoney error \n') 
                 MyLog.error(str(e) +  '\n')

              


      def updateSpeed(self,stock):
          data = stock.get_data()
          last_line = stock.get_Lastline()
          l = stock.len()
          for i in [10, 40, 100]:
              pos = l
              if i < l:
                 pos = i
              df_temp = data.tail(pos)    
              for index,row in df_temp.iterrows(): 
                  if float(row['open']) != 0.0:
                     p = (float(last_line.get('price')) - float(row['price'])) / float(row['open']) * 100 
                     stock.set_speed('s' + str(i),p) 
                     break  


      def updateSpeedCount(self,stock,conf):
          self.updateSpeed(stock)
          data = stock.get_data()
          last_line = stock.get_Lastline()
          pre_pos = conf['speed']['near_pos']
          if pre_pos > stock.len():
             pre_pos = stock.len() 
          df_temp = data.tail(pre_pos)
          for index,row in df_temp.iterrows():
              if float(row['open']) != 0.0:
                 p = (float(last_line.get('price')) - float(row['price'])) / float(row['open']) * 100 
                 stock.set_near_speed(p)
                 break
          last_second_line = stock.get_LastSecondline()
          p = (float(last_line.get('price')) - float(last_second_line.get('price'))) / float(last_line.get('open')) * 100 
          if p >= conf['speed']['min_single_p'] or p <= conf['speed']['min_single_p'] * -1:
             stock.add_total_speed(p)     

      def convertToFloat(self,str):
          try:
              return float(str)
          except Exception as e:
                 MyLog.error('convertToFloat error: ' + str + '\n') 
                 return 0   


      def theLastIsSellOrBuy(self,stock):
          lastLine = stock.get_Lastline()
          lastSeconfLine = stock.get_LastSecondline()
          last_amount = float(lastLine.get('amount'))
          last_sec_amount = float(lastSeconfLine.get('amount'))
          if last_sec_amount == last_amount:
             return 'no_deal' 
          last_price = float(lastLine.get('price'))  
          last_b_p_1 = float(lastLine.get('b1_p'))
          last_b_v_1 = self.convertToFloat(lastLine.get('b1_v'))
          last_a_p_1 = float(lastLine.get('a1_p'))
          last_a_v_1 = self.convertToFloat(lastLine.get('a1_v'))
          last_sec_price = float(lastSeconfLine.get('price'))
          last_sec_b_p_1 = float(lastSeconfLine.get('b1_p'))
          last_sec_b_v_1 = self.convertToFloat(lastSeconfLine.get('b1_v'))
          last_sec_a_p_1 = float(lastSeconfLine.get('a1_p'))
          last_sec_a_v_1 = self.convertToFloat(lastSeconfLine.get('a1_v'))
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
          big_amount = self.__config.get_t1()['big_money']['amount']
          big_volume = self.__config.get_t1()['big_money']['volume']
          type = self.theLastIsSellOrBuy(stock)
          if type == 'drive_buy':
             if amount >= big_amount or volume >= big_volume:
                stock.addNetBuy(last_amount - last_sec_amount)  
             if amount >= conf['big_money']['single_amount']:
                 stock.addBigMoneyTotalAmount(amount)
             if volume >= conf['big_money']['single_volume']:
                 stock.addBigMoneyTotalVolume(volume) 
          elif type == 'drive_sell':
               if amount >= big_amount or volume >= big_volume:
                  stock.addNetBuy(last_sec_amount - last_amount)           

             
      def updateBreakRtimes(self,stock,conf):
          now_p = self.getCurrentPercent(stock)
          lastSecondLine = stock.get_LastSecondline()
          last_p = self.getPercent(lastSecondLine.get('price'),stock)
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
              if t1[key]['open_p'][0] < open_p and open_p < t1[key]['open_p'][1]:
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
          data = stock.get_data()
          if stock.len() < 3:
             return False 
          price = float(data.iloc[-1].get('price'))
          price2 = float(data.iloc[-2].get('price'))
          price3 = float(data.iloc[-2].get('price')) 
          return price - price2 > 0 and price2 - price3 >= 0
          


      def isPeedMatch(self,stock,conf):
          flag = stock.get_near_speed() >= conf['speed']['threshold'] or stock.get_total_speed() >= conf['speed']['threshold']
          if flag == True:
             MyLog.info('*** ' + stock.get_code() + ' match speed ***') 
             MyLog.info('near speed ' + str(stock.get_near_speed()))
             MyLog.info('total speed ' + str(stock.get_total_speed()))
          return flag    

      def isBigMoneyMatch(self,stock,conf):
          flag = stock.getBigMoneyTotalAmount() >= conf['big_money']['total_amount'] or stock.getBigMoneyTotalVolume() >= conf['big_money']['total_volume']
          if flag == True:
             MyLog.info('*** ' + stock.get_code() + ' match big_money ***') 
             MyLog.info('big money amount ' + str(stock.getBigMoneyTotalAmount()))
             MyLog.info('big money volume ' + str(stock.getBigMoneyTotalVolume()))  
          return flag     

      def isNetMatch(self,stock,conf):
          return stock.get_net() >= conf['big_money']['net']



      def isTimeMatch(self,conf):
          now = dt.datetime.now()
          timeStr = now.strftime('%H:%M:%S')
          return timeStr <= conf['time']


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


      def isReachMinR(self,stock):
          now_p = self.getCurrentPercent(stock)
          minR = stock.get_minR()
          return now_p > stock.get_r_val(minR)

              


              
