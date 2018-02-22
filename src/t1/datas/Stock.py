# -*-coding=utf-8-*-

__author__ = 'aqua'

import pandas as pd
import datetime as dt
from ..MyLog import MyLog
import datetime as dt

class Stock(object):

      def __init__(self, code, data):
          self.__code = code
          self.__minR = None
          self.__rBreakTimes = {
              'R1' : {
                 'val' : -10,
                 'b_times' : 0
              },
              'R2' : {
                 'val' : -10,
                 'b_times' : 0
              },
              'R3' : {
                 'val' : -10,
                 'b_times' : 0 
              },
              'R4' : {
                 'val' : -10,
                 'b_times' : 0 
              },
              'R5' : {
                 'val' : -10,
                 'b_times' : 0  
              }
          }
          self.__speed = {
              'v300' : 0,
              'v120' : 0,
              'v30' : 0
          }
          self.__bigMoney = {
               'total_amount' : 0,
               'total_volume' : 0,
               'in' : 0,
               'out' : 0
          }
          self.__netBuy = 0
          self.__priceVolumeMap = {
              'last_volume' : 0,
              'last_time' : None,
              'pvMap' : []
          }
          if isinstance(data, pd.Series):
             self.__data = pd.DataFrame([data])
          elif isinstance(data, pd.DataFrame):
               self.__data = data


      def getPriceVolumeMap(self):
          return self.__priceVolumeMap['pvMap']


      def addPriceVolumeMap(self,date,time,price,volume):
          nowDateTime = dt.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S') 
          if self.__priceVolumeMap['last_time'] is not None:
             if (nowDateTime - self.__priceVolumeMap['last_time']).seconds < 30:
                return 
          self.__priceVolumeMap['last_time'] = nowDateTime
          vol = volume - self.__priceVolumeMap['last_volume']
          self.__priceVolumeMap['last_volume'] = volume
          self.__priceVolumeMap['pvMap'].append({'price' : price,'volume' : vol})


      def get_speed(self,key):
          return self.__speed[key]

      def set_speed(self,key,speed):
          self.__speed[key] = speed         
                 
      def set_minR(self,minR):
          self.__minR = minR

      def get_minR(self):
          return self.__minR               

      def addNetBuy(self,net):
          self.__netBuy = self.__netBuy + net

      def get_net(self):
          return self.__netBuy    

      def addBigMoneyIn(self,inAmount):  
          self.__bigMoney['in'] = self.__bigMoney['in'] + inAmount

      def getBigMoneyIn(self):
          return self.__bigMoney['in'] 

      def addBigMoneyOut(self,outAmount):  
          self.__bigMoney['out'] = self.__bigMoney['out'] + outAmount 

      def getBigMoneyOut(self):
          return self.__bigMoney['out']       


      def set_r_val(self,key,val):
          self.__rBreakTimes[key]['val'] = val

      def get_r_val(self,key):
          return self.__rBreakTimes[key]['val']          

      def add_rBreakTimes(self,key):
          self.__rBreakTimes[key]['b_times'] = self.__rBreakTimes[key]['b_times'] + 1

      def get_rBreakTimes(self,key):
          return self.__rBreakTimes[key]['b_times']   

      def set_minR(self,minR):
          self.__minR = minR

      def get_minR(self):
          return self.__minR               

      def get_code(self):
          return self.__code

      def get_data(self):
          return self.__data   

      def len(self):
          if self.__data is None:
             return 0 
          return len(self.__data)  


      def get_LastSecondline(self):
          if self.len() < 2:
             return None
          return self.__data.iloc[-2]  

      def get_Lastline(self):
          if self.len() == 0:
             return None
          return self.__data.iloc[-1]    

      def add_Line(self,row):
          lastLine = self.get_Lastline()
          if lastLine is not None:
             lastTime = lastLine.get('time') 
             last_date = dt.datetime.strptime(lastLine['date'] + ' ' + lastTime, '%Y-%m-%d %H:%M:%S')
             if lastTime != row['time']:
                self.__data = self.__data.append(row) 
                row_date = dt.datetime.strptime(row['date'] + ' ' + row['time'], '%Y-%m-%d %H:%M:%S') 
                if row['time'] >= '09:30:00' and (row_date - last_date).seconds > 3:
                   MyLog.warn('%s get data is more than 3s,now = %s %s,last = %s %s' % (row['code'],row['date'],row['time'],lastLine['date'],lastLine['time'])) 