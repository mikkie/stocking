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
import threading

class Analyze(object):
    
      def __init__(self):
          self.__config = Config()
          self.__engine = create_engine(self.__config.get_DBurl())
 
      def calcMain(self,dh):
          data = dh.get_data()
          finalCode = ''
          result = []
          for code in data:
              if len(dh.get_buyed()) > 0:
                 if code in dh.get_buyed():
                    continue 
              try:  
                 if self.calc(data[code],dh):
                    result.append(data[code])
              except Exception as e:
                     last_line = data[code].get_Lastline()
                     MyLog.error(last_line['time'] + ' :calc ' + code + ' error')
                     MyLog.error(str(e))      
          if len(result) != 0:
             try:
                df_res = self.goTopsis(result)
                finalCode = self.outputRes(df_res)
                self.saveData(finalCode,result)
             except Exception as e:
                    codes = []
                    for stock in result:
                        codes.append(stock.get_code())
                    MyLog.error('calc topsis error %s' % codes)
                    MyLog.error(str(e))   
          return finalCode   


      def save(self,data):
          try: 
              code = data.iloc[0]['code']
              data.to_sql('live_' + code, con = self.__engine, if_exists='replace', index=False)
          except Exception as e:
                 MyLog.error('save [%s] data error \n' % code)
                 MyLog.error(str(e) +  '\n')

      def saveData(self,code,result):
          for stock in result:
              if code == stock.get_code():
                 data = stock.get_data()
                 t = threading.Thread(target=self.save, args=(data,)) 
                 t.start()  
                 break

      def outputRes(self,df_res):
          df_final = df_res.iloc[0]
          trade = self.__config.get_t1()['trade']
          info = '[%s] 在 %s 以 %s 买入 [%s]%s %s 股' % (Utils.getCurrentTime(),str(df_final['date']) + ' ' + str(df_final['time']), str(float(df_final['price']) + trade['addPrice']), df_final['code'], df_final['name'], str(trade['volume']))
          MyLog.info(info)
          print(info)
          return df_final['code']       


      def goTopsis(self,result):
          df = pd.DataFrame()
          for stock in result:
              df = self.buildData(df,stock)
          return self.topsisCalc(df)    


      def topsisCalc(self,df):
          df = df.fillna(df.mean())   
          self.commonCalc(df,'net',self.__config.get_t1()['topsis']['net'],True)
          self.commonCalc(df,'v120',self.__config.get_t1()['topsis']['v120'],True)
          self.commonCalc(df,'v300',self.__config.get_t1()['topsis']['v300'],True)
          self.commonCalc(df,'v30',self.__config.get_t1()['topsis']['v30'],True)
          self.commonCalc(df,'r_break',self.__config.get_t1()['topsis']['r_break'],False)
          for index,row in df.iterrows():
              self.calcDi(df,index,row,['net','v120','v300','v30','r_break'],'_best')
              self.calcDi(df,index,row,['net','v120','v300','v30','r_break'],'_worst')
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
          data.loc[data['time'] == last_line['time'], 'v300'] = stock.get_speed('v300')
          data.loc[data['time'] == last_line['time'], 'v120'] = stock.get_speed('v120')
          data.loc[data['time'] == last_line['time'], 'v30'] = stock.get_speed('v30')
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
          

              
      def calc(self,stock,dh):
          if not self.canCalc(stock,dh):
             return False 
          open_p = self.getOpenPercent(stock)
          conf = self.getConfig(open_p)  
          if conf is None:
             dh.add_buyed(stock.get_code(),False) 
             return False 
          self.initStockData(stock,open_p,conf)
          self.updateStock(stock,conf)  
          return self.isStockMatch(stock,conf)   


    #   def isJHJJMatch(self,stock,dh):
    #       lastLine = stock.get_Lastline()
    #       now_time = lastLine['time']
    #       if now_time >= '09:30:00':
    #          return True 
    #       if stock.len() >= 2:
    #          lastSecondLine = stock.get_LastSecondline()
    #          if now_time > '09:17:00' and now_time < '09:20:00':
    #             b1_v = self.convertToFloat(lastLine.get('b1_v'))
    #             b1_amount = float(lastLine.get('b1_p')) * b1_v * 100
    #             lastB1_v = self.convertToFloat(lastSecondLine.get('b1_v'))
    #             lastB1_amount = float(lastSecondLine.get('b1_p')) * lastB1_v * 100
    #             if b1_v < lastB1_v * 0.5 or b1_amount < lastB1_amount * 0.5:
    #                dh.add_buyed(stock.get_code(),True)
    #                return False
    #          if now_time > '09:24:30' and now_time < '09:25:03':  
    #             b1_v = self.convertToFloat(lastLine.get('b1_v'))
    #             b1_amount = float(lastLine.get('b1_p')) *  b1_v * 100
    #             if b1_v <= 1000 or b1_amount <= 3000000:
    #                dh.add_buyed(stock.get_code(),True) 
    #                return False
    #          return True      
    #       return False

      def isOpenMatch(self,row):
          if float(row['pre_close']) == 0 or float(row['open']) == 0:
             return False
          return (float(row['open']) - float(row['pre_close'])) / float(row['pre_close']) * 100 >= -1.0

      def isOpenMatch2(self,row):
          if float(row['settlement']) == 0 or float(row['open']) == 0:
             return False
          return (float(row['open']) - float(row['settlement'])) / float(row['settlement']) * 100 >= -1.0  
              
                   


      def canCalc(self,stock,dh):
          if stock.len() < 0:
             return False
        #   if not self.isJHJJMatch(stock,dh):
        #      return False    
          lastLine = stock.get_Lastline() 
          if float(lastLine.get('open')) == 0.0:
             return False
          lastSecondLine = stock.get_LastSecondline()
          if lastSecondLine is None:
             return False  
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
          self.updateSpeed(stock)
          try:
             self.updateBigMoney(stock,conf)
          except Exception as e:
                 MyLog.error('updateBigMoney error \n') 
                 MyLog.error(str(e) +  '\n')

              


      def updateSpeed(self,stock):
          data = stock.get_data()
          last_line = stock.get_Lastline()
          now_time = dt.datetime.strptime(last_line['date'] + ' ' + last_line['time'], '%Y-%m-%d %H:%M:%S')
          l = stock.len()
          for i in [30, 120, 300]:
              pos = l
              if int(i/3) + 1 < l:
                 pos = int(i/3) + 1
              df_temp = data.tail(pos)    
              for index,row in df_temp.iterrows(): 
                  if float(row['open']) != 0.0:
                     row_time = dt.datetime.strptime(row['date'] + ' ' + row['time'], '%Y-%m-%d %H:%M:%S') 
                     deltaS = (now_time - row_time).seconds
                     if deltaS == 0:
                        stock.set_speed('v' + str(i),0)
                        break 
                     if deltaS <= i and deltaS >= i - 6:
                        p = (float(last_line.get('price')) - float(row['price'])) / float(row['pre_close']) * 100 
                        stock.set_speed('v' + str(i),p / deltaS) 
                        # print('speed %s = %f' % ('v' + str(i),p / deltaS))
                        break  

      def convertToFloat(self,str):
          if str == '':
             return 0 
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
          now_time = dt.datetime.strptime(lastLine['date'] + ' ' + lastLine['time'], '%Y-%m-%d %H:%M:%S')
          lastSeconfLine = stock.get_LastSecondline()
          last_time = dt.datetime.strptime(lastSeconfLine['date'] + ' ' + lastSeconfLine['time'], '%Y-%m-%d %H:%M:%S')
          last_amount = float(lastLine.get('amount'))
          last_sec_amount = float(lastSeconfLine.get('amount'))
          last_volume = float(lastLine.get('volume'))
          last_sec_volume = float(lastSeconfLine.get('volume'))
          amount = last_amount - last_sec_amount
          volume = last_volume - last_sec_volume
          big_amount = self.__config.get_t1()['big_money']['amount']
          big_volume = self.__config.get_t1()['big_money']['volume']
        #   print('price=%s,amount=%s' % (lastLine['price'],amount))
        #   if amount >= big_amount or volume >= big_volume:
          type = self.theLastIsSellOrBuy(stock)
          if type == 'drive_buy': 
             stock.addBigMoneyIn(last_amount - last_sec_amount)
            #  print('in = %f' % stock.getBigMoneyIn())
             stock.addNetBuy(last_amount - last_sec_amount)
            #  print('net = %f' % stock.get_net())
          elif type == 'drive_sell':  
               stock.addBigMoneyOut(last_amount - last_sec_amount)
               stock.addNetBuy(last_sec_amount - last_amount)  
            #    print('net = %f' % stock.get_net())
          
             
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
              if t1[key]['open_p'][0] <= open_p and open_p < t1[key]['open_p'][1]:
                 return t1[key] 

      def isStockMatch(self,stock,conf):
          if not self.isTimeMatch(stock,conf):
             return False
          if not self.isReachMinR(stock):
             return False
          if not self.isNetMatch(stock,conf):
             return False      
          if stock.get_minR() != 'R5':
             if not self.isSpeedMatch(stock,conf) or not self.isBigMoneyMatch(stock,conf):
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
          
      def isSpeedMatch(self,stock,conf):
          v30 = stock.get_speed('v30')
          v120 = stock.get_speed('v120')
          v300 = stock.get_speed('v300')
          p = self.getCurrentPercent(stock)
          v_list = [v30,v120,v300]
          flag = False
          if v_list[0] * 30 >= (10 - p) * self.__config.get_t1()['speed']['v30_ratio']:
             flag = True    
          elif v_list[0] >= self.__config.get_t1()['speed']['v30'] and (v_list[1] >= self.__config.get_t1()['speed']['v120'] or v_list[2] >= self.__config.get_t1()['speed']['v300']):
               flag = True
          if flag == True:
             last_line = stock.get_Lastline() 
             info = '[%s] *** [%s] match speed at %s %s,v30=%s,v120=%s,v300=%s ***' % (Utils.getCurrentTime(),stock.get_code(),last_line['date'],last_line['time'],str(v30),str(v120),str(v300))
             MyLog.info(info)
             print(info)
          return flag    


      def isBigMoneyMatch(self,stock,conf):
          flag = stock.get_net() / stock.getBigMoneyIn() > self.__config.get_t1()['big_money']['threshold']
          if flag == True:
             last_line = stock.get_Lastline() 
             info = '[%s] *** [%s] match big_money at %s %s,net=%s,in=%s ***' % (Utils.getCurrentTime(),stock.get_code(),last_line['date'],last_line['time'],str(stock.get_net()),str(stock.getBigMoneyIn()))
             MyLog.info(info) 
             print(info)
          return flag     

      def isNetMatch(self,stock,conf):
          last_line = stock.get_Lastline()
          return stock.get_net() >= conf['big_money']['net'] * float(last_line['price'])


      def isTimeMatch(self,stock,conf):
          lastLine = stock.get_Lastline()
          timeStr = lastLine['time']
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

              


              
