# -*-coding=utf-8-*-
__author__ = 'aqua'

from .Stock import Stock

import threading
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import datetime as dt
import time
import sys
sys.path.append('../..')
from config.Config import Config 
from t1.MyLog import MyLog
from concurrent.futures import ThreadPoolExecutor

class DataHolder(object):

      def __init__(self,codes):  
          self.__data = {}
          self.__buyed = []
          self.__selled = []
          self.__setting = Config()
          self.__tpe = ThreadPoolExecutor(5)
          self.__engine = create_engine(self.__setting.get_DBurl()) 

      def get_buyed(self):
          return self.__buyed

      def get_selled(self):
          return self.__selled 

      def add_selled(self,code,save=False):
          self.__selled.append(code)
          if save:
             self.__tpe.submit(self.saveData,self.__data[code].get_data())   

      def add_buyed(self,code,save=False):
          self.__buyed.append(code)
          if save:
             self.__tpe.submit(self.saveData,self.__data[code].get_data())

      def get_data(self):
          return self.__data


      def addDataHandler(self,row):
          code = row['code']
          if code in self.get_buyed():
             return 
          if code in self.__data and self.__data[code].len() > 0:
             self.__data[code].add_Line(row)
          else:
               self.__data[code] = Stock(code,row)
          if float(row['pre_close']) != 0 and (float(row['price']) - float(row['pre_close'])) / float(row['pre_close']) * 100 >= 9.9:
             if not (code in self.get_buyed()): 
                MyLog.info('[%s] reach 10' % code) 
                self.add_buyed(code,True)


      def addSellDataHandler(self,row):
          code = row['code']
          if code in self.get_selled():
             return
          if code in self.__data and self.__data[code].len() > 0:
             self.__data[code].add_Line(row)
          else:
               self.__data[code] = Stock(code,row)


      def addData(self,df):
          df.apply(self.addDataHandler,axis=1)


      def addSellData(self,df):
          df.apply(self.addSellDataHandler,axis=1)    

      def saveData(self,data):
          try: 
              line = data[0]
              code = line['code']
              df = pd.DataFrame(data)
              df.to_sql('live_' + code, con = self.__engine, if_exists='replace', index=False)
              MyLog.info('[%s] save data' % code)
          except Exception as e:
                 MyLog.error('[%s %s] save [%s] data error \n' % (line['date'],line['time'],code))
                 MyLog.error(str(e) +  '\n')
 