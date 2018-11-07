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

   code_pre_close_map = [('000608', '5.02'), ('000609', '5.45'), ('000622', '6.08'), ('000638', '4.79'), ('000939', '1.12'), ('000953', '3.9'), ('002054', '5.63'), ('002058', '10.25'), ('002098', '8.14'), ('002102', '1.75'), ('002141', '3.49'), ('002188', '3.02'), ('002194', '4.86'), ('002260', '3.4'), ('002261', '3.91'), ('002263', '1.73'), ('002432', '5.35'), ('002625', '7.84'), ('002793', '10.49'), ('002796', '24.1'), ('002800', '18.64'), ('002840', '13.58'), ('002888', '19.78'), ('300025', '4.05'), ('300126', '5.12'), ('300221', '5.72'), ('300289', '6.03'), ('300310', '4.06'), ('300584', '22.66'), ('300674', '8.36'), ('300730', '21.57'), ('600232', '4.76'), ('600238', '4.53'), ('600490', '4.9'), ('600532', '5.61'), ('600610', '1.47'), ('600689', '9.5'), ('600695', '5.83'), ('600701', '2.55'), ('600744', '2.71'), ('603016', '17.04'), ('603032', '33.75'), ('603040', '26.85'), ('603718', '13.61')]
   date = '20181107'
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
          
           





