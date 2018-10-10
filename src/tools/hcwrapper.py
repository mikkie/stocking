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

   code_pre_close_map = [('000662', '5.96'), ('002199', '6.8'), ('002207', '5.27'), ('002427', '11.34'), ('002476', '4.97'), ('002501', '3.64'), ('002629', '5.0'), ('002856', '18.92'), ('002895', '11.76'), ('002898', '16.8'), ('002915', '24.65'), ('002931', '38.84'), ('300089', '5.69'), ('300257', '9.98'), ('300281', '5.51'), ('300503', '8.71'), ('300514', '10.45'), ('300644', '33.8'), ('300670', '12.77'), ('300690', '16.43'), ('600074', '1.23'), ('600532', '4.79'), ('601011', '5.55'), ('603032', '22.06'), ('603320', '16.11'), ('603356', '15.23'), ('603538', '16.65'), ('603722', '31.7'), ('603798', '10.27'), ('603895', '24.81')]
   date = '20181009'
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
          
           





