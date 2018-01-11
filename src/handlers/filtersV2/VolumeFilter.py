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

          df_h_long = data['df_h'][1:4]
          df_h_short = data['df_h'][0:2]

          #前3天量都不超过前一天2倍
          nextVolume = None
          vol3 = df_h_long.iloc[2].get('volume')
          vol2 = df_h_long.iloc[1].get('volume')
          vol1 = df_h_long.iloc[0].get('volume') 
          vol0 = df_h_short.iloc[0].get('volume')
          open = df_h_short.iloc[0].get('open')
          close = df_h_short.iloc[0].get('close')
          w = 1
          if vol2 > vol3 * config.get_Volume()[0]:
             w = 0.9
          if vol1 > vol2 * config.get_Volume()[0]: 
             if w == 0.9:
                w = 0.7
             w = 0.8      
          if close <= open:
             data['volume'] = 0
             return False 
          data['volume'] = w * vol0 / vol1
          return vol0 > vol1 * config.get_Volume()[1]