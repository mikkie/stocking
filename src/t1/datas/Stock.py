# -*-coding=utf-8-*-

__author__ = 'aqua'

import pandas as pd

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
              'near_speed_count' : 0,
              'total_speed_count' : 0,
              's100' : 0,
              's40' : 0,
              's10' : 0
          }
          self.__bigMoney = {
               'total_amount' : 0,
               'total_volume' : 0
          }
          self.__netBuy = 0
          if isinstance(data, pd.Series):
             self.__data = pd.DataFrame([data])
          elif isinstance(data, pd.DataFrame):
               self.__data = data

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


      def addBigMoneyTotalAmount(self,amount):
          self.__bigMoney['total_amount'] = self.__bigMoney['total_amount'] + amount  


      def getBigMoneyTotalAmount(self):
          return self.__bigMoney['total_amount']


      def getBigMoneyTotalVolume(self):
          return self.__bigMoney['total_volume']       


      def addBigMoneyTotalVolume(self,volume):
          self.__bigMoney['total_volume'] = self.__bigMoney['total_volume'] + volume


      def set_near_speed(self,val):
          self.__speed['near_speed_count'] = val


      def get_near_speed(self):
          return self.__speed['near_speed_count']

      def add_total_speed(self,val):
          self.__speed['total_speed_count'] = self.__speed['total_speed_count'] + val     

    
      def get_total_speed(self):
          return self.__speed['total_speed_count']


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
             if lastTime != row['time']:
                self.__data = self.__data.append(row) 