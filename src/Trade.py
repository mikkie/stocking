# -*-coding=utf-8-*-

__author__ = 'aqua'

import tushare as ts
import time
import threading

def monitoring():
    print(ts.get_realtime_quotes(['002839','000885']))
    timer = threading.Timer(2, monitoring)
    timer.start()

timer = threading.Timer(2, monitoring)
timer.start()
while True:
      time.sleep(0.01)
pass
