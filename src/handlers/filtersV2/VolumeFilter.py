# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import sys
sys.path.append('..')
from utils.Utils import Utils

class VolumeFilter(object):
      pass

      def filter(self, data, config):
          if not ('df_h' in data) or data['df_h'].empty :
             def cb(**kw):
                 return ts.get_hist_data(kw['kw']['code'])
             data['df_h'] = Utils.queryData('h_data_' + data['df_3m'].iloc[0]['code'],'code',data['engine'], cb, forceUpdate=config.get_updateToday(),code=data['df_3m'].iloc[0]['code'])   

          df_h_long = data['df_h'][config.get_Volume()[0]:config.get_Volume()[1]]
          df_h_short = data['df_h'][0:config.get_Volume()[0]]

          for index,row in df_h_long.iterrows(): 
              if row['volume'] > row['v_ma10'] * config.get_Volume()[2]:
                 return False 

          for index,row in df_h_short.iterrows():
              if row['volume'] < row['v_ma10'] * config.get_Volume()[3]:
                 return False
          return True      