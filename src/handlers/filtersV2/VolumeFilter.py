# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts

class VolumeFilter(object):
      pass

      def filter(self, data, config):
          if data['df_h'] is None or data['df_h'].empty :
             data['df_h'] = ts.get_hist_data(data.iloc[0]['code'])
          df_last_3h = data['df_h'][0:3]
          for index,row in df_last_3h.iterrows():
              if row['volume'] < row['v_ma10']:
                 return False
          return True      