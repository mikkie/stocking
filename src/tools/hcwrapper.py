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

   code_pre_close_map = [('000707', '2.44'), ('000757', '4.6'), ('000803', '10.95'), ('002034', '9.75'), ('002072', '6.28'), ('002188', '2.71'), ('002209', '6.13'), ('002213', '7.21'), ('002263', '1.17'), ('002333', '7.16'), ('002423', '7.75'), ('002445', '2.46'), ('002451', '6.4'), ('002504', '2.63'), ('002576', '8.24'), ('002591', '5.45'), ('002667', '6.23'), ('002723', '7.65'), ('002724', '5.07'), ('002726', '7.51'), ('002846', '10.57'), ('002865', '16.8'), ('002940', '23.07'), ('300104', '2.76'), ('300116', '1.49'), ('300240', '6.86'), ('300547', '15.97'), ('300586', '11.85'), ('300670', '19.07'), ('300692', '13.36'), ('300736', '28.11'), ('600191', '3.91'), ('600247', '3.64'), ('600311', '2.81'), ('600610', '1.29'), ('600687', '4.23'), ('600766', '7.03'), ('600774', '10.38'), ('603032', '22.47'), ('603088', '10.89')]
   date = '20181023'
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
          
           





