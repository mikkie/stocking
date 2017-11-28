# -*-coding=utf-8-*-
__author__ = 'aqua'

import numpy as np
import tushare as ts
import sys
sys.path.append('..')
from utils.Utils import Utils

class LongFlatFilter(object):
      pass

      def filter(self, data, config):
          if not ('df_h' in data) or data['df_h'].empty :
             def cb(**kw):
                 return ts.get_hist_data(kw['kw']['code'])
             data['df_h'] = Utils.queryData('h_data_' + data['df_3m'].iloc[0]['code'],'code',data['engine'], cb, forceUpdate=config.get_updateToday(),code=data['df_3m'].iloc[0]['code'])
          if data['df_h'] is None or len(data['df_h']) < config.get_FlatTrade()[0]:
             return False 
          df_h_10 = data['df_h'][0:config.get_FlatTrade()[1]]
          high_row_10 = df_h_10.loc[df_h_10['close'].idxmax()]
          high_10 = high_row_10.get('close')

          df_h_90 = data['df_h'][config.get_FlatTrade()[1]:config.get_FlatTrade()[0]]
          high_row_90 = df_h_90.loc[df_h_90['close'].idxmax()]
          high_90 = high_row_90.get('close')
          low_row_90 = df_h_90.loc[df_h_90['close'].idxmin()]
          low_90 = low_row_90.get('close')
          if high_10 == 0 or high_90 == 0 or low_90 == 0:
             return False        
          return high_10 / low_90 > config.get_FlatTrade()[3] and high_90 / low_90 < config.get_FlatTrade()[2]