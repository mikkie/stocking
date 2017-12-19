# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import datetime as dt
import sys
sys.path.append('..')
from utils.Utils import Utils

class TurnoverFilter(object):
      pass

      def filter(self, data, config):
          if not ('df_h' in data) or data['df_h'].empty :
             def cb(**kw):
                 return ts.get_hist_data(kw['kw']['code'])
             data['df_h'] = Utils.queryData('h_data_' + data['df_3m'].iloc[0]['code'],'code',data['engine'], cb, forceUpdate=config.get_updateToday(),code=data['df_3m'].iloc[0]['code'])   
          df_h_3 = data['df_h'][0:3]
          for index,row in df_h_3.iterrows(): 
              if row['turnover'] < config.get_TurnOver():
                 return False
          return True     