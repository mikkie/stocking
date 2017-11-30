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

          df_h_90 = data['df_h'][config.get_Volume()[0]:config.get_Volume()[1]]
          avg_90 = df_h_90['volume'].mean()

          df_h_3 = data['df_h'][0:config.get_Volume()[0]]
          avg_3 = df_h_3['volume'].mean()

          if avg_3 >= avg_90 * config.get_Volume()[2]:
             return True
           
          df_last_3h = data['df_h'][0:3]
          for index,row in df_last_3h.iterrows():
              if row['volume'] < row['v_ma10']:
                 return False
          return True      