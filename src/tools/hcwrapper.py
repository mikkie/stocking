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

   code_pre_close_map = [('000006', '5.07'), ('000498', '4.27'), ('000586', '9.57'), ('000662', '5.72'), ('000760', '3.58'), ('000852', '10.64'), ('000893', '4.08'), ('002010', '9.08'), ('002016', '9.42'), ('002058', '10.12'), ('002122', '1.68'), ('002248', '6.99'), ('002259', '4.13'), ('002297', '8.0'), ('002312', '3.44'), ('002336', '8.26'), ('002427', '11.18'), ('002532', '4.67'), ('002607', '6.86'), ('002692', '5.32'), ('002795', '14.12'), ('002796', '28.15'), ('002936', '4.59'), ('300004', '3.99'), ('300056', '5.51'), ('300077', '7.75'), ('300084', '5.4'), ('300240', '6.86'), ('300293', '7.92'), ('300345', '4.79'), ('300483', '23.85'), ('300503', '8.81'), ('600207', '5.43'), ('600234', '7.03'), ('600856', '4.65'), ('603036', '12.58')]
   date = '20180919'
   date_next = '20180920'
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
          
           





