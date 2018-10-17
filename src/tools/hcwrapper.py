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

   code_pre_close_map = [('000498', '4.37'), ('000606', '5.98'), ('000616', '2.49'), ('000670', '2.79'), ('002011', '3.66'), ('002095', '20.9'), ('002306', '2.38'), ('002356', '9.55'), ('002447', '2.67'), ('002569', '8.71'), ('002681', '3.32'), ('002785', '7.38'), ('002795', '15.39'), ('002845', '13.43'), ('002853', '18.72'), ('300117', '3.05'), ('300131', '4.35'), ('300296', '6.64'), ('300434', '11.22'), ('300468', '11.73'), ('300493', '9.2'), ('300501', '14.79'), ('300508', '18.7'), ('300561', '13.42'), ('300668', '20.85'), ('300671', '18.1'), ('300708', '10.1'), ('300716', '12.61'), ('300736', '19.2'), ('600080', '8.6'), ('600093', '7.05'), ('600311', '2.69'), ('600385', '8.6'), ('600520', '12.25'), ('600532', '4.38'), ('600536', '22.75'), ('600715', '4.15'), ('600766', '6.48'), ('600845', '17.4'), ('603105', '13.83'), ('603516', '21.4'), ('603555', '6.0'), ('603657', '35.87'), ('603798', '11.4'), ('603978', '20.9')]
   date = '20181017'
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
          
           





