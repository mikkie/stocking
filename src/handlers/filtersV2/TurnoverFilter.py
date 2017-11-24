# -*-coding=utf-8-*-
__author__ = 'aqua'

class TurnoverFilter(object):
      pass

      def filter(self, data, config):
          df_realTime = data['df_realTime']
          return df_realTime['turnoverratio'] > config.get_TurnOver()