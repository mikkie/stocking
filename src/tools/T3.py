# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import threading
import time
import sys
sys.path.append('..')
from trade.DataHolder import DataHolder

code = '000615'
dh = DataHolder()
df = ts.get_tick_data(code,date='2018-01-12')
length = len(df)
i = length - 1

def monitoring(i):
    if i >= 0:
       dh.add_data(code,df.iloc[i]) 
       print(dh.get_data(code))
    i = i - 1
    timer = threading.Timer(3, monitoring,[i])
    timer.start()

timer = threading.Timer(3, monitoring,[i])
timer.start()
while True:
      time.sleep(0.01)
pass
