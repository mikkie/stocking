# -*-coding=utf-8-*-

__author__ = 'aqua'
from models.Stock import Stock 
import numpy as np

class MACDFeature(object):
      
      def calcFeatureValue(self, stock:Stock):
          kdata = stock.get_kdata() 
          yesterday = kdata.iloc[-2].get('macd')
          lastday = kdata.iloc[-3].get('macd')
          now = kdata.iloc[-1].get('macd')
          if np.isnan(yesterday) or np.isnan(now) or np.isnan(lastday):
             return False 
          return (yesterday < 0 and lastday < 0 and yesterday > lastday) and (now > 0 or round(float(now), 2) == 0.00)