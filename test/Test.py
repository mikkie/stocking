# -*-coding=utf-8-*-
__author__ = 'aqua'

import pandas as pd
import tushare as ts
import threading
import time

df = ts.get_realtime_quotes(['601901'])
one = df.iloc[0]
a = int(round(time.time() * 1000))
df2 = pd.DataFrame([one]) 
print('time1 = %d' % (int(round(time.time() * 1000)) - a)) 