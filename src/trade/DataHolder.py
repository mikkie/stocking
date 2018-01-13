# -*-coding=utf-8-*-
__author__ = 'aqua'

import pandas as pd

class DataHolder(object):
      pass

      def __init__(self):  
          self.__data = {}

      def get_data(self,code):
          if code in self.__data:
             return self.__data[code]
          return None

      def init_data(self,code,df):
          self.__data[code] = df

      def add_data(self,code,row):
          change = row['change']
          if change == '--':
             change = 0.0 
          data = {'time' : row['time'], 'price' : float(row['price']), 'change' : float(change), 'volume' : int(row['volume']), 'amount' : float(row['amount']), 'types' : row['type']}
          if code in self.__data and self.__data[code] is not None:
             self.__data[code] = self.__data[code].append(data,ignore_index=True)
          else:
             self.__data[code] = pd.DataFrame([data])
                  

                  
