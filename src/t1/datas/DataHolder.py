# -*-coding=utf-8-*-
__author__ = 'aqua'

from .Stock import Stock

import threading
import pandas as pd
from sqlalchemy import create_engine
import sys
sys.path.append('../..')
from config.Config import Config 

class DataHolder(object):

      def __init__(self,needSaveData):  
          self.__data = {}
          if needSaveData:
             self.__setting = Config()
             self.__engine = create_engine(self.__setting.get_DBurl()) 
             global timer 
             timer = threading.Timer(10, self.saveData)
             timer.start() 

      def get_data(self):
          return self.__data

      def addData(self,df):
          for index,row in df.iterrows():
              code = row['code']
              if code in self.__data and self.__data[code].len() > 0:
                 self.__data[code].add_Line(row)
              else:
                 self.__data[code] = Stock(code,row)

      def saveData(self):
          for code in self.__data:
              df = self.__data[code].get_data()
              if df is not None and len(df) > 0:
                 df.to_sql('live_' + code, con = self.__engine, if_exists='replace')
          timer = threading.Timer(10, self.saveData)
          timer.start()           
 