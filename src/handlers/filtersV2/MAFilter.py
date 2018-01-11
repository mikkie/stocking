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
          score = 0
          w = 9
          for index,row in df_last_90h.iterrows():   
              if row['open'] >= row['ma5']:
                 score = score + 2 * w
              elif row['open'] >= row['ma10']: 
                   score = score + 1 * w
              w = w - 1
              if w < 1:
                 w = 1     
          data['ma'] = score       
          close = df_last_90h.iloc[0].get('close')
          open = df_last_90h.iloc[0].get('open')
          ma5 = df_last_90h.iloc[0].get('ma5')
          ma10 = df_last_90h.iloc[0].get('ma10')
          if close <= open:
             return False
          return open >= ma5 and open > ma10
