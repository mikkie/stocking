# -*-coding=utf-8-*-

__author__ = 'aqua'

import pandas as pd

class Stock(object):

      def __init__(self, code, row):
          self.__code = code
          self.__data = pd.DataFrame([row])

      def get_code(self):
          return self.__code

      def get_data(self):
          return self.__data   

      def len(self):
          if self.__data is None:
             return 0 
          return len(self.__data)  

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