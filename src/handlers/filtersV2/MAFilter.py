# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts

class MAFilter(object):
      pass 

      def filter(self, data, config):
          if data['df_h'] is None or data['df_h'].empty :
             data['df_h'] = ts.get_hist_data(data.iloc[0]['code'])
          df_last_90h = data['df_h'][0:90]
          count_higher_ma5 = 0
          count_higher_ma10 = 0
          for index,row in df_last_90h.iterrows():   
              if row['close'] >= row['ma5']:
                 count_higher_ma5 = count_higher_ma5 + 1
              if row['close'] >= row['ma10']:    
                 count_higher_ma10 = count_higher_ma10 + 1
          return count_higher_ma5 / 90 > config.get_KLineMA()[0] and count_higher_ma10 / 90 > config.get_KLineMA()[1]     
