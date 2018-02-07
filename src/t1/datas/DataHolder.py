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

class DataHolder(object):

      def __init__(self,codes):  
          self.__data = {}
          self.__buyed = []
          self.__setting = Config()
          self.__engine = create_engine(self.__setting.get_DBurl()) 
          if self.__setting.get_t1()['need_recover_data'] and self.needRecoverData():
             self.recoverData(codes) 

      def recoverData(self,codes):
          for code in codes:
              try:
                 src_data = pd.read_sql_table('live_' + code, con = self.__engine) 
                 if src_data is not None and len(src_data) > 0:
                    last = src_data.iloc[-1]
                    now_date = time.strftime('%Y-%m-%d',time.localtime(time.time())) 
                    if now_date == last['date']:
                       self.__data[code] = Stock(code,src_data) 
              except Exception as e:
                     MyLog.error('recover data error \n')
                     MyLog.error(str(e) +  '\n')

      def needRecoverData(self):
          now = dt.datetime.now()
          return now > dt.datetime(now.year,now.month,now.day,9,15)     

      def get_buyed(self):
          return self.__buyed

      def add_buyed(self,code):
          self.__buyed.append(code)        

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
          if (float(row['price']) - float(row['pre_close'])) / float(row['pre_close']) * 100 >= 9.3:
             t = threading.Thread(target=self.saveData, args=(self.__data[code].get_data(),)) 
             t.start()


      def addData(self,df):
          df.apply(self.addDataHandler,axis=1)

      def saveData(self,data):
          try: 
              code = data.iloc[0]['code']
              data.to_sql('live_' + code, con = self.__engine, if_exists='replace', index=False)
          except Exception as e:
                 MyLog.error('save [%s] data error \n' % code)
                 MyLog.error(str(e) +  '\n')
 