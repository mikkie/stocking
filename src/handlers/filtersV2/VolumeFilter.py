# -*-coding=utf-8-*-
__author__ = 'aqua'

class VolumeFilter(object):
      pass

      def filter(self, data, config):
          df_last_3h = data['df_h'][0:3]
          for index,row in df_last_3h.iterrows():
              if row['volume'] < row['v_ma10']:
                 return False
          return True      