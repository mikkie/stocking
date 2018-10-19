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

   code_pre_close_map = [('000509', '2.47'), ('000606', '5.49'), ('000662', '6.48'), ('000971', '3.41'), ('002366', '8.71'), ('002786', '5.6'), ('002857', '10.34'), ('002860', '17.0'), ('002865', '15.2'), ('002923', '25.3'), ('300009', '12.64'), ('300434', '10.83'), ('300461', '19.84'), ('300503', '9.11'), ('300559', '32.5'), ('300578', '13.23'), ('300586', '10.1'), ('300589', '12.11'), ('300595', '30.45'), ('300640', '9.02'), ('300647', '16.16'), ('300668', '15.66'), ('300670', '17.01'), ('300683', '26.3'), ('300690', '17.3'), ('300717', '19.67'), ('300727', '19.87'), ('600532', '4.8'), ('600766', '4.86'), ('603013', '19.26'), ('603032', '24.53'), ('603058', '9.72'), ('603320', '17.54'), ('603356', '16.26'), ('603367', '14.65'), ('603798', '10.69'), ('603895', '24.78')]
   date = '20181012'
   date_next = '20181015'
   load_dir = '../../data/excels'
   compare_dir = '../../data/compare'

   hcdata.removeall(load_dir)
   code_list = download.download(code_pre_close_map, date, load_dir)
   df_list = hcdata.loaddata(load_dir, save=False)
   result = hitTopTest2.start_test_by_df(df_list)
   if len(result) > 0:
      hcdata.removeall(compare_dir)
      download.download(result, date_next, compare_dir) 
      compare_list = hcdata.loaddata(compare_dir, save=False)
      if len(compare_list) > 0:
         for res in result:
             for df in compare_list:
                 if df.iloc[0]['code'] == res[0]:
                    avg = (df.iloc[0]['price'] + df.iloc[-1]['price'] + df['price'].min() + df['price'].max()) / 4
                    print('[%s] buyed price=%s, next day: avg=%s, open=%s, close=%s, low=%s, high=%s' % (res[0], res[1], avg, df.iloc[0]['price'], df.iloc[-1]['price'], df['price'].min(), df['price'].max()))
                    continue 
          
           





