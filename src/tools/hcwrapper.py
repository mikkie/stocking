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

   code_pre_close_map = [('000532', '8.48'), ('000593', '8.1'), ('000606', '6.61'), ('000659', '3.21'), ('000669', '7.11'), ('000760', '3.57'), ('000903', '2.48'), ('000913', '8.71'), ('000917', '4.34'), ('000931', '5.99'), ('000936', '4.71'), ('002054', '4.65'), ('002072', '6.3'), ('002102', '1.69'), ('002122', '1.65'), ('002137', '6.56'), ('002263', '1.57'), ('002357', '6.24'), ('002420', '3.35'), ('002452', '3.9'), ('002647', '14.3'), ('002687', '6.47'), ('002700', '11.1'), ('002800', '17.95'), ('002843', '14.69'), ('002862', '22.0'), ('300091', '3.74'), ('300169', '4.11'), ('300270', '6.67'), ('300508', '29.38'), ('300670', '17.21'), ('300688', '39.06'), ('300730', '21.79'), ('600053', '14.4'), ('600064', '6.75'), ('600082', '3.73'), ('600107', '5.38'), ('600128', '6.07'), ('600133', '4.81'), ('600165', '3.78'), ('600182', '16.37'), ('600210', '3.02'), ('600235', '4.24'), ('600247', '4.17'), ('600275', '2.51'), ('600283', '9.72'), ('600290', '3.78'), ('600333', '6.02'), ('600438', '7.03'), ('600462', '2.78'), ('600599', '10.22'), ('600604', '3.52'), ('600621', '7.96'), ('600624', '4.4'), ('600635', '3.41'), ('600689', '7.85'), ('600695', '5.37'), ('600701', '2.34'), ('600718', '10.84'), ('600736', '5.01'), ('600751', '3.14'), ('600783', '9.8'), ('600796', '5.36'), ('600856', '4.74'), ('600895', '9.81'), ('601012', '15.9'), ('601222', '4.49'), ('603032', '32.89'), ('603085', '8.26'), ('603188', '9.26'), ('603507', '17.04'), ('603800', '11.97'), ('603861', '9.2')]
   date = '20181105'
   date_next = '20181015'
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
          
           





