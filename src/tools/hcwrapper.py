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

   code_pre_close_map = [('000017', '4.24'), ('000505', '5.23'), ('000566', '5.56'), ('000982', '1.39'), ('002122', '1.69'), ('002219', '3.96'), ('002813', '23.18'), ('002930', '28.17'), ('002931', '32.1'), ('300023', '9.2'), ('300085', '9.58'), ('300281', '4.55'), ('300392', '7.14'), ('300731', '26.15'), ('600010', '1.51'), ('600421', '5.24'), ('600532', '3.95'), ('600614', '4.68'), ('600617', '5.76'), ('600636', '11.11'), ('600733', '9.5'), ('600746', '6.18'), ('600896', '3.74'), ('603013', '18.07'), ('603790', '31.33'), ('603969', '4.77')]
   date = '20180928'
   date_next = '20180920'
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
          
           





