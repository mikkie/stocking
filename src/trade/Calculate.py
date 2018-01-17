# -*-coding=utf-8-*-
__author__ = 'aqua'

import pandas as pd
import math

class Calculate(object):
      pass

      def __init__(self):
          self.__i = 0

      def calc(self,codeList,dh):
          dataList = []
          for code in codeList:
              df = dh.get_data(code)
              if df is not None and self.__i < len(df):
                 dataList.append(df.iloc[self.__i])
          if len(dataList) > 0:
             res = pd.DataFrame(dataList) 
             print(res)
             self.__i = self.__i + 1
          