# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import threading
import time

def calculate():
    df = ts.get_realtime_quotes(['603289','000615'])
    print(df[['name','ask','a1_v','bid','b1_v','price', 'volume','amount','open','pre_close','high','low','code','time']]) 
    timer2 = threading.Timer(2, calculate)
    timer2.start()

timer2 = threading.Timer(2, calculate)
timer2.start()

while True:
      time.sleep(0.01)
pass

