# -*-coding=utf-8-*-

__author__ = 'aqua'

import tushare as ts
import time
import threading

def monitoring():
    df = ts.get_realtime_quotes(['002839','000885'])
    print(df[['code','name','price','bid','ask','b1_v','b1_p','a1_v','a1_p','volume','amount','time']])
    timer = threading.Timer(2, monitoring)
    timer.start()

timer = threading.Timer(2, monitoring)
timer.start()
while True:
      time.sleep(0.01)
pass
