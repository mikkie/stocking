# -*-coding=utf-8-*-
__author__ = 'aqua'

import download
import hcdata
import hitTopTest2

"""
   This is for test
"""

if __name__ == '__main__':
   # code_pre_close_map = [('000760','3.58')]
   # date = '20180919'

   code_pre_close_map = [('000509', '2.91'), ('000610', '7.19')]
   date = '20180920'

   hcdata.removeall()
   code_list = download.download(code_pre_close_map, date)
   df_list = hcdata.loaddata(save=False)
   hitTopTest2.start_test_by_df(df_list)





