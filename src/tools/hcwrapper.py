# -*-coding=utf-8-*-
__author__ = 'aqua'

import download
import hcdata
import hitTopTest2
import datetime as dt
from datetime import timedelta
"""
   This is for test
"""

if __name__ == '__main__':
   # code_pre_close_map = [('000760','3.58')]
   # date = '20180919'

   code_pre_close_map = [('000498', '5.02'), ('000576', '6.39'), ('000756', '5.97'), ('000760', '3.93'), ('000793', '2.98'), ('000931', '6.59'), ('000936', '5.18'), ('002066', '7.15'), ('002137', '7.22'), ('002141', '3.17'), ('002192', '14.85'), ('002208', '9.92'), ('002263', '1.65'), ('002328', '4.98'), ('002423', '8.38'), ('002427', '14.65'), ('002489', '2.72'), ('002529', '7.38'), ('002575', '4.74'), ('002655', '5.77'), ('002700', '12.21'), ('002881', '16.1'), ('002888', '17.98'), ('300100', '8.29'), ('300390', '8.44'), ('300624', '59.81'), ('300760', '102.42'), ('600064', '7.43'), ('600069', '3.0'), ('600133', '5.29'), ('600165', '4.16'), ('600235', '4.66'), ('600247', '4.38'), ('600257', '4.3'), ('600290', '4.16'), ('600321', '1.78'), ('600366', '4.83'), ('600532', '5.1'), ('600620', '5.48'), ('600630', '7.13'), ('600647', '11.32'), ('600679', '11.62'), ('600784', '4.96'), ('600848', '19.23'), ('600981', '4.42'), ('603366', '3.55')]
   date = '20181106'
   date_next = '20181015'
   load_dir = '../../data/excels'
   compare_dir = '../../data/compare'

#    hcdata.removeall(load_dir)
#    code_list = download.download(code_pre_close_map, date, load_dir)
   df_list = hcdata.loaddata(load_dir, save=False)
   result = hitTopTest2.start_test_by_df(df_list)
#    if len(result) > 0:
#       hcdata.removeall(compare_dir)
#       download.download(result, date_next, compare_dir) 
#       compare_list = hcdata.loaddata(compare_dir, save=False)
#       if len(compare_list) > 0:
#          for res in result:
#              for df in compare_list:
#                  if df.iloc[0]['code'] == res[0]:
#                     avg = (df.iloc[0]['price'] + df.iloc[-1]['price'] + df['price'].min() + df['price'].max()) / 4
#                     print('[%s] buyed price=%s, next day: avg=%s, open=%s, close=%s, low=%s, high=%s' % (res[0], res[1], avg, df.iloc[0]['price'], df.iloc[-1]['price'], df['price'].min(), df['price'].max()))
#                     continue 
          
           





