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

   code_pre_close_map = [('000533', '3.24'), ('000576', '5.8'), ('000659', '2.75'), ('000669', '6.09'), ('000806', '3.79'), ('002427', '11.91'), ('002629', '5.5'), ('002700', '9.7'), ('002860', '15.93'), ('002863', '6.07'), ('002877', '13.63'), ('002893', '17.36'), ('002895', '12.94'), ('002903', '21.46'), ('002931', '42.72'), ('300023', '9.15'), ('300335', '7.35'), ('300394', '19.34'), ('300514', '11.5'), ('300522', '16.94'), ('300641', '5.59'), ('300670', '14.05'), ('300692', '12.85'), ('300716', '11.82'), ('300717', '16.25'), ('600462', '2.77'), ('600520', '12.0'), ('603032', '24.27'), ('603041', '14.19'), ('603177', '10.02'), ('603183', '18.03'), ('603188', '8.51'), ('603192', '38.64'), ('603223', '11.97'), ('603320', '17.72'), ('603607', '17.19'), ('603633', '9.91')]
   date = '20181010'
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
          
           





