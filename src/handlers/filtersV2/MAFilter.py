# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import sys
sys.path.append('..')
from utils.Utils import Utils

class MAFilter(object):
      pass 

      def filter(self, data, config):
          if not ('df_h' in data) or data['df_h'].empty :
             def cb(**kw):
                 return ts.get_hist_data(kw['kw']['code'])
             data['df_h'] = Utils.queryData('h_data_' + data['df_3m'].iloc[0]['code'],'code',data['engine'], cb, forceUpdate=config.get_updateToday(),code=data['df_3m'].iloc[0]['code']) 
          df_last_3h = data['df_h'][0:3]
          for index,row in df_last_3h.iterrows():   
              if row['close'] < row['ma5']:
                 return False
          return True      
              
