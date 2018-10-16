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

   code_pre_close_map = [('000509', '2.54'), ('000587', '2.27'), ('000593', '7.4'), ('000616', '2.26'), ('002700', '10.87'), ('002795', '13.99'), ('002830', '17.48'), ('002856', '20.19'), ('300216', '4.9'), ('300266', '3.14'), ('300411', '8.18'), ('300514', '13.97'), ('300581', '11.0'), ('300667', '22.48'), ('300668', '18.95'), ('300760', '48.8'), ('600385', '7.82'), ('600766', '5.89'), ('603330', '18.32'), ('603555', '5.45'), ('603586', '10.94'), ('603633', '10.16'), ('603657', '32.61')]
   date = '20181016'
   date_next = '20180929'
   load_dir = '../../data/excels'
   compare_dir = '../../data/compare'

   hcdata.removeall(load_dir)
   code_list = download.download(code_pre_close_map, date, load_dir)
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
          
           





