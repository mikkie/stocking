# -*-coding=utf-8-*-
__author__ = 'aqua'

import pandas as pd
import tushare as ts
import datetime as dt

array = []
df = ts.get_realtime_quotes(['600053'])
now = dt.datetime.now()
for i in range(3000):
    array.append(df.iloc[0])
print((dt.datetime.now() - now).seconds)    
df = pd.DataFrame([df.iloc[0]])
now = dt.datetime.now()
for i in range(3000):
    df.append(df.iloc[0])
print((dt.datetime.now() - now).seconds)
now = dt.datetime.now()
all = None
for i in range(3000):
    all = pd.concat([df.iloc[0]])
print((dt.datetime.now() - now).seconds)  