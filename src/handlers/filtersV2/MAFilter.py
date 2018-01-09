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
          df_last_90h = data['df_h'][0:config.get_KLineMA()[0]]
          count_higher_ma5 = 0
          count_higher_ma10 = 0
          for index,row in df_last_90h.iterrows():   
              if row['close'] >= row['ma5']:
                 count_higher_ma5 = count_higher_ma5 + 1
              if row['close'] >= row['ma10']:    
                 count_higher_ma10 = count_higher_ma10 + 1
          return count_higher_ma5 / 3 > config.get_KLineMA()[1] and count_higher_ma10 / 3 > config.get_KLineMA()[2]     
