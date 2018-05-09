# -*-coding=utf-8-*-

__author__ = 'aqua'

import pandas as pd
import datetime as dt
from ..MyLog import MyLog
import datetime as dt

class NewStock(object):

      def __init__(self, code, data):
          self.__code = code
          self.__minR = None
          self.__ls = None
          self.__inited = False
          self.__sellSignal = 0
          self.__buySignal = 0
          self.__time = None
          self.__lowerThanBeforeTimes = 0
          self.__cache = {
              'ocp' : None
          }
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
          self.__data = [data.to_dict()]

      def is_inited(self):
          return self.__inited

      def set_inited(self):
          self.__inited = True  

      def get_cache(self,key):
          return self.__cache[key]

      def set_cache(self,key,val):
          self.__cache[key] = val  

      def get_lowerThanBeforeTimes(self):
          return self.__lowerThanBeforeTimes

      def add_lowerThanBeforeTimes(self):
          self.__lowerThanBeforeTimes = self.__lowerThanBeforeTimes + 1

      def set_time(self,time):
          self.__time = time

      def get_time(self):
          return self.__time         

      def set_minR(self,minR):
          self.__minR = minR

      def get_minR(self):
          return self.__minR           

      def set_ls(self,ls):
          self.__ls = ls

      def get_ls(self):
          return self.__ls

      def get_sellSignal(self):
          return self.__sellSignal

      def get_buySignal(self):
          return self.__buySignal  

      def add_sellSignal(self):
          self.__sellSignal = self.__sellSignal + 1

      def add_buySignal(self):
          self.__buySignal = self.__buySignal + 1    

      def reset_sellSignal(self):
          self.__sellSignal = 0      

      def reset_buySignal(self):
          self.__buySignal = 0              

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
          return self.__data[-2]  

      def get_Lastline(self):
          if self.len() == 0:
             return None
          return self.__data[-1]    

      def add_Line(self,row):
          lastLine = self.get_Lastline()
          if lastLine is not None:
             lastTime = lastLine['time'] 
             last_date = dt.datetime.strptime(lastLine['date'] + ' ' + lastTime, '%Y-%m-%d %H:%M:%S')
             if lastTime != row['time']:
                self.__data.append(row.to_dict())
            #  now = dt.datetime.now()
            #  if self.get_time() is not None:
            #     deltaSeconds = (now - self.get_time()).seconds
            #     if deltaSeconds > 3:
            #        print('[%s] calc more than %s s' % (self.get_code(),deltaSeconds)) 
            #  self.set_time(now) 