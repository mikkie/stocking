# -*-coding=utf-8-*-

__author__ = 'aqua'

import pandas as pd

class Stock(object):

      def __init__(self, code, data):
          self.__code = code
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
              'total_speed_count' : 0
          },
          if isinstance(data, pd.Series):
             self.__data = pd.DataFrame([data])
          elif isinstance(data, pd.DataFrame):
               self.__data = data
                 

      def set_near_speed(self,val):
          self.__speed['near_speed_count'] = val

      def add_total_speed(self,val):
          self.__speed['total_speed_count'] = self.__speed['total_speed_count'] + val     

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