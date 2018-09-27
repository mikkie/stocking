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

   code_pre_close_map = [('000006', '5.58'), ('000017', '3.96'), ('000422', '2.63'), ('000498', '4.7'), ('000662', '6.29'), ('000707', '2.75'), ('000721', '4.35'), ('000893', '4.28'), ('000962', '6.28'), ('002002', '3.0'), ('002057', '6.31'), ('002164', '3.12'), ('002213', '9.29'), ('002229', '6.2'), ('002261', '4.25'), ('002357', '6.48'), ('002532', '5.14'), ('002586', '4.7'), ('002604', '1.73'), ('002667', '6.29'), ('300019', '6.05'), ('300071', '3.65'), ('300090', '2.99'), ('300092', '8.2'), ('300127', '12.12'), ('300135', '2.8'), ('300340', '13.18'), ('600112', '3.29'), ('600366', '5.0'), ('600462', '2.7'), ('601689', '15.26'), ('603032', '25.5'), ('603058', '9.42'), ('603917', '13.26')]
   date = '20180920'
   date_next = '20180921'
   load_dir = '../../data/excels'
   compare_dir = '../../data/compare'

#    hcdata.removeall(load_dir)
#    code_list = download.download(code_pre_close_map, date, load_dir)
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
                    print('[%s] buy price=%s, open=%s, close=%s, low=%s, max=%s' % (res[0], res[1], df.iloc[0]['price'], df.iloc[-1]['price'], df['price'].max(), df['price'].min()))
                    continue 
          
           





