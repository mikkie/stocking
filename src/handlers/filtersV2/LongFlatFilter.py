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
          df_h = data['df_h'][config.get_FlatTrade()[0] * -1:]
          high_row = df_h.loc[df_h['high'].idxmax()]
          high = high_row.get('high')
          low_row = df_h.loc[df_h['low'].idxmin()]
          low = low_row.get('low')
          count = 0
          for index,row in df_h.iterrows():
              p_change = row['p_change']
              if abs(p_change) < 3.00:
                 count = count + 1
          if high == 0 or low == 0:
             return False        
          return count >= config.get_FlatTrade()[0] * config.get_FlatTrade()[1] and (high - low)/low < config.get_FlatTrade()[2]  