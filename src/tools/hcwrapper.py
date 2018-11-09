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

   code_pre_close_map = [('000068', '2.64'), ('000409', '4.22'), ('000509', '3.18'), ('000605', '7.34'), ('000626', '6.63'), ('000638', '5.8'), ('000939', '1.24'), ('000995', '5.72'), ('002067', '3.27'), ('002122', '1.89'), ('002260', '3.75'), ('002417', '7.57'), ('002477', '1.74'), ('002547', '3.41'), ('002575', '6.3'), ('002660', '5.6'), ('002680', '2.94'), ('002692', '4.12'), ('002708', '5.56'), ('300041', '6.72'), ('300299', '3.87'), ('300505', '24.07'), ('300549', '11.83'), ('300590', '22.64'), ('300653', '47.86'), ('300703', '14.5'), ('300751', '56.68'), ('600082', '4.49'), ('600133', '5.89'), ('600212', '3.7'), ('600250', '6.8'), ('600275', '2.68'), ('600283', '11.6'), ('600462', '4.08'), ('600463', '6.1'), ('600493', '5.76'), ('600610', '1.62'), ('600658', '5.06'), ('600666', '3.19'), ('600683', '4.08'), ('600689', '11.5'), ('600701', '2.81'), ('600791', '3.84'), ('600817', '6.77'), ('600870', '2.7'), ('603058', '11.65'), ('603269', '16.34'), ('603386', '18.26'), ('603389', '9.24'), ('603499', '22.99'), ('603758', '6.23'), ('603803', '8.59')]
   date = '20181109'
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
          
           





