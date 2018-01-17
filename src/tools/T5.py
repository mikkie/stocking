# -*-coding=utf-8-*-
__author__ = 'aqua'

import tushare as ts
import math
import threading
import time
import pandas as pd
from datetime import datetime

datas = {}

def calculate():
    df = ts.get_realtime_quotes(['300698','000617','601375','002736','300708','603611'])
    df[['price','pre_close']] = df[['price','pre_close']].apply(pd.to_numeric)
    df['percent'] = (df['price'] - df['pre_close']) / df['pre_close'] * 100
    df = df.sort_values(by='percent',ascending=False)
    print(df)

    timer2 = threading.Timer(1, calculate)
    timer2.start()

timer2 = threading.Timer(1, calculate)
timer2.start()

while True:
      time.sleep(0.01)
pass