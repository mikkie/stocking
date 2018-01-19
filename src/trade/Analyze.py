# -*-coding=utf-8-*-
__author__ = 'aqua'


class Analyze(object):

      def calc(self, datas):
          for code in datas:
              self.start(datas[code])

      def start(self, data):
          if self.open_type(data['data']) == 'High_open':
             print(data['data'])

      def open_type(self, df):
          open_df = df.loc[df['time'] == '09:25:03']
          if len(open_df) == 0:
             return 'pending' 
          row = open_df.iloc[0]  
          if float(row['open']) == 0:
             return 'stop' 
          open_p = (float(row['price']) - float(row['pre_close'])) / float(row['pre_close']) * 100
          # 高开
          if open_p > 4.0:
             return 'High_open'
          # 平开
          elif open_p > -1.0 and open_p < 1.0:
               return 'Flat_open'            
